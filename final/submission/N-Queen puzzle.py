from gurobipy import Model, GRB, quicksum
import matplotlib.pyplot as plt
import csv
import random


class NQueensSolver:
    def __init__(self, n):
        self.n = n  # 皇后数量
        self.solutions = []
        self.unique_set = set()

    def solve_all(self):
        model = Model("n_queens_all")
        # 参数设置，确保搜全解
        model.setParam("OutputFlag", 0)  # 关闭日志
        model.setParam("LazyConstraints", 1)  # 开启惰性约束
        model.setParam("MIPGap", 0)  # 精确求解
        model.setParam("MIPFocus", 2)  # 加强可行解搜索
        model.setParam("PoolSearchMode", 2)  # 搜索多个解
        model.setParam("PoolSolutions", 1000)  # 允许存储足够多解
        model.setParam("Cuts", 3)  # 开启剪枝
        model.setParam("Presolve", 0)  # 禁用预处理避免简化导致漏解
        model.setParam("Threads", 1)  # 单线程保证稳定

        # 创建变量 x[i,j]，表示第i行第j列是否放置皇后
        x = {
            (i, j): model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")
            for i in range(self.n)
            for j in range(self.n)
        }
        model.update()

        # 每行恰好放一个皇后
        for i in range(self.n):
            model.addConstr(quicksum(x[i, j] for j in range(self.n)) == 1)
        # 每列恰好放一个皇后
        for j in range(self.n):
            model.addConstr(quicksum(x[i, j] for i in range(self.n)) == 1)
        # 主对角线（从左上到右下）最多一个皇后
        for d in range(-self.n + 1, self.n):
            model.addConstr(
                quicksum(
                    x[i, j] for i in range(self.n) for j in range(self.n) if i - j == d
                )
                <= 1
            )
        # 副对角线（从右上到左下）最多一个皇后
        for d in range(2 * self.n - 1):
            model.addConstr(
                quicksum(
                    x[i, j] for i in range(self.n) for j in range(self.n) if i + j == d
                )
                <= 1
            )

        # 设置一个恒定目标函数，仅为求可行解
        model.setObjective(0, GRB.MAXIMIZE)

        # 回调函数用于收集所有不同解
        def callback(model, where):
            if where == GRB.Callback.MIPSOL:
                sol = model.cbGetSolution(x)
                pos = [(i, j) for (i, j), val in sol.items() if val > 0.5]
                key = frozenset(pos)
                if key in self.unique_set:
                    return
                self.unique_set.add(key)
                self.solutions.append(pos)
                # 添加惰性约束排除当前解，避免重复
                model.cbLazy(
                    quicksum(
                        (1 - x[i, j] if (i, j) in pos else x[i, j])
                        for i in range(self.n)
                        for j in range(self.n)
                    )
                    >= 1
                )

        model.optimize(callback)

    def visualize(self, idx=0, save=False, filename="solution.png"):
        if not self.solutions:
            print("未找到解")
            return
        if idx >= len(self.solutions):
            print(f"无效索引：{idx}")
            return

        n = self.n
        fig, ax = plt.subplots(figsize=(n, n))
        for i in range(n):
            for j in range(n):
                color = "cornsilk" if (i + j) % 2 == 0 else "gray"
                ax.add_patch(plt.Rectangle((j, n - 1 - i), 1, 1, facecolor=color))
        for i, j in self.solutions[idx]:
            ax.text(
                j + 0.5,
                n - 1 - i + 0.5,
                "♛",
                ha="center",
                va="center",
                fontsize=28,
                color="crimson",
            )
        ax.set_xlim(0, n)
        ax.set_ylim(0, n)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")
        if save:
            plt.savefig(filename, bbox_inches="tight")
        else:
            plt.show()
        plt.close()

    def is_valid_solution(self, positions):
        """验证给定的皇后位置是否为有效解"""
        if len(positions) != self.n:
            return False, "皇后数量不正确"

        # 检查行和列的唯一性
        rows = [pos[0] for pos in positions]
        cols = [pos[1] for pos in positions]

        if len(set(rows)) != self.n:
            return False, "存在行冲突"
        if len(set(cols)) != self.n:
            return False, "存在列冲突"

        # 检查对角线冲突
        for i in range(self.n):
            for j in range(i + 1, self.n):
                r1, c1 = positions[i]
                r2, c2 = positions[j]

                # 主对角线冲突
                if r1 - c1 == r2 - c2:
                    return False, f"主对角线冲突: ({r1},{c1}) 和 ({r2},{c2})"

                # 副对角线冲突
                if r1 + c1 == r2 + c2:
                    return False, f"副对角线冲突: ({r1},{c1}) 和 ({r2},{c2})"

        return True, "有效解"

    def generate_random_arrangements(self, num_samples=50):
        """生成随机的8皇后排列用于验证"""
        arrangements = []

        # 生成一些真实的解
        if self.solutions:
            # 从已找到的解中随机选择一些
            real_solutions = random.sample(self.solutions, min(10, len(self.solutions)))
            for i, sol in enumerate(real_solutions):
                arrangements.append(
                    {
                        "ID": i + 1,
                        "Type": "Valid",
                        "Positions": str(sol),
                        "Row_0": sol[0][1],
                        "Row_1": sol[1][1],
                        "Row_2": sol[2][1],
                        "Row_3": sol[3][1],
                        "Row_4": sol[4][1],
                        "Row_5": sol[5][1],
                        "Row_6": sol[6][1],
                        "Row_7": sol[7][1],
                        "Expected_Valid": True,
                    }
                )

        # 生成随机排列（大部分是无效的）
        start_id = len(arrangements) + 1
        for i in range(num_samples - len(arrangements)):
            # 随机生成皇后位置
            cols = list(range(self.n))
            random.shuffle(cols)
            positions = [(row, cols[row]) for row in range(self.n)]

            is_valid, reason = self.is_valid_solution(positions)

            arrangements.append(
                {
                    "ID": start_id + i,
                    "Type": "Random",
                    "Positions": str(positions),
                    "Row_0": positions[0][1],
                    "Row_1": positions[1][1],
                    "Row_2": positions[2][1],
                    "Row_3": positions[3][1],
                    "Row_4": positions[4][1],
                    "Row_5": positions[5][1],
                    "Row_6": positions[6][1],
                    "Row_7": positions[7][1],
                    "Expected_Valid": is_valid,
                }
            )

        return arrangements

    def save_arrangements_to_csv(self, filename="queens_test_data.csv", num_samples=50):
        """保存随机排列到CSV文件"""
        arrangements = self.generate_random_arrangements(num_samples)

        fieldnames = [
            "ID",
            "Type",
            "Row_0",
            "Row_1",
            "Row_2",
            "Row_3",
            "Row_4",
            "Row_5",
            "Row_6",
            "Row_7",
            "Expected_Valid",
            "Positions",
        ]

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(arrangements)

        # 统计信息
        valid_count = sum(1 for arr in arrangements if arr["Expected_Valid"])
        invalid_count = len(arrangements) - valid_count

        print(f"CSV文件已保存: {filename}")
        print(f"数据统计:")
        print(f"   - 总样本数: {len(arrangements)}")
        print(f"   - 有效解: {valid_count}")
        print(f"   - 无效解: {invalid_count}")
        print(f"   - 有效率: {valid_count/len(arrangements)*100:.1f}%")

        return filename

    def verify_csv_data(self, filename="queens_test_data.csv"):
        """验证CSV文件中的数据"""
        print(f"\n 验证CSV文件: {filename}")

        correct_predictions = 0
        total_predictions = 0

        with open(filename, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # 构建位置列表
                positions = []
                for i in range(8):
                    col = int(row[f"Row_{i}"])
                    positions.append((i, col))

                # 验证
                is_valid, reason = self.is_valid_solution(positions)
                expected = row["Expected_Valid"].lower() == "true"

                if is_valid == expected:
                    correct_predictions += 1
                else:
                    print(
                        f"ID {row['ID']}: 预期 {expected}, 实际 {is_valid} - {reason}"
                    )

                total_predictions += 1

        accuracy = correct_predictions / total_predictions * 100
        print(f"验证完成:")
        print(f"   - 正确预测: {correct_predictions}/{total_predictions}")
        print(f"   - 准确率: {accuracy:.1f}%")

        return accuracy


if __name__ == "__main__":
    # 创建求解器并求解8皇后问题
    solver = NQueensSolver(8)
    solver.solve_all()
    print(f"共找到 {len(solver.solutions)} 个解")

    # 生成CSV测试数据
    print("\n 生成测试数据...")
    csv_file = solver.save_arrangements_to_csv(
        "queens_verification_data.csv", num_samples=100
    )

    # 验证生成的数据
    print("\n🔬 验证生成的数据...")
    accuracy = solver.verify_csv_data(csv_file)

    # 保存前两个解的图片
    print("\n 保存解的可视化...")
    solver.visualize(0, save=True, filename="nqueen_solution1.png")
    solver.visualize(1, save=True, filename="nqueen_solution2.png")

    print(f"\n 任务完成! 生成了 {csv_file} 用于验证算法正确性")

    # 显示前几行数据作为示例
    print("\n CSV数据示例:")
    with open(csv_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:6]):  # 显示前6行
            print(f"   {line.strip()}")
        if len(lines) > 6:
            print(f"   ... (还有 {len(lines)-6} 行)")
