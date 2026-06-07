"""
N-Queens Solver using Gurobi MIP with Lazy Constraints

Finds *all* solutions to the N-Queens problem by:
  1. Formulating a binary MIP (one queen per row, column, and diagonal).
  2. Using a Gurobi callback to collect each feasible solution found.
  3. Adding a lazy cut after each solution to exclude it from future search,
     ensuring the solver enumerates every distinct placement.

Usage:
    python "N-Queen puzzle.py"
"""

import csv
import pathlib
import random

import matplotlib.pyplot as plt
from gurobipy import GRB, Model, quicksum


class NQueensSolver:
    """Solve the N-Queens problem and enumerate all distinct solutions."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.solutions: list[list[tuple[int, int]]] = []
        self._seen: set[frozenset] = set()

    # ── Solver ────────────────────────────────────────────────────────────────

    def solve_all(self) -> None:
        """Enumerate all N-Queens solutions via Gurobi pool search + lazy cuts."""
        model = Model("n_queens_all")
        model.setParam("OutputFlag", 0)
        model.setParam("LazyConstraints", 1)
        model.setParam("MIPGap", 0)
        model.setParam("MIPFocus", 2)
        model.setParam("PoolSearchMode", 2)
        model.setParam("PoolSolutions", 1000)
        model.setParam("Cuts", 3)
        model.setParam("Presolve", 0)
        model.setParam("Threads", 1)

        # x[i, j] = 1  iff a queen is placed in row i, column j
        x = {
            (i, j): model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")
            for i in range(self.n)
            for j in range(self.n)
        }
        model.update()

        # Exactly one queen per row
        for i in range(self.n):
            model.addConstr(quicksum(x[i, j] for j in range(self.n)) == 1)

        # Exactly one queen per column
        for j in range(self.n):
            model.addConstr(quicksum(x[i, j] for i in range(self.n)) == 1)

        # At most one queen per main diagonal (top-left → bottom-right)
        for d in range(-(self.n - 1), self.n):
            model.addConstr(
                quicksum(
                    x[i, j]
                    for i in range(self.n)
                    for j in range(self.n)
                    if i - j == d
                )
                <= 1
            )

        # At most one queen per anti-diagonal (top-right → bottom-left)
        for d in range(2 * self.n - 1):
            model.addConstr(
                quicksum(
                    x[i, j]
                    for i in range(self.n)
                    for j in range(self.n)
                    if i + j == d
                )
                <= 1
            )

        model.setObjective(0, GRB.MAXIMIZE)

        def _callback(model, where):
            if where != GRB.Callback.MIPSOL:
                return
            sol = model.cbGetSolution(x)
            positions = frozenset((i, j) for (i, j), v in sol.items() if v > 0.5)
            if positions in self._seen:
                return
            self._seen.add(positions)
            self.solutions.append(sorted(positions))
            # Lazy cut: exclude this exact placement from future solutions
            model.cbLazy(
                quicksum(
                    (1 - x[i, j]) if (i, j) in positions else x[i, j]
                    for i in range(self.n)
                    for j in range(self.n)
                )
                >= 1
            )

        model.optimize(_callback)

    # ── Visualisation ─────────────────────────────────────────────────────────

    def visualize(
        self,
        idx: int = 0,
        *,
        save: bool = False,
        filename: str = "solution.png",
    ) -> None:
        """Draw a chessboard with the queens for solution number `idx`."""
        if not self.solutions:
            print("No solutions found.")
            return
        if idx >= len(self.solutions):
            print(f"Index {idx} out of range (only {len(self.solutions)} solutions).")
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
        ax.set_title(f"{n}-Queens — Solution {idx + 1}")

        if save:
            plt.savefig(filename, bbox_inches="tight")
        else:
            plt.show()
        plt.close()

    # ── Validation ────────────────────────────────────────────────────────────

    def is_valid(self, positions: list[tuple[int, int]]) -> tuple[bool, str]:
        """Return (True, 'valid') or (False, reason) for a queen placement."""
        if len(positions) != self.n:
            return False, f"Expected {self.n} queens, got {len(positions)}"

        rows = [r for r, _ in positions]
        cols = [c for _, c in positions]

        if len(set(rows)) != self.n:
            return False, "Row conflict"
        if len(set(cols)) != self.n:
            return False, "Column conflict"

        for a in range(self.n):
            for b in range(a + 1, self.n):
                r1, c1 = positions[a]
                r2, c2 = positions[b]
                if r1 - c1 == r2 - c2:
                    return False, f"Main-diagonal conflict: ({r1},{c1}) vs ({r2},{c2})"
                if r1 + c1 == r2 + c2:
                    return False, f"Anti-diagonal conflict: ({r1},{c1}) vs ({r2},{c2})"

        return True, "valid"

    # ── CSV export / verification ──────────────────────────────────────────────

    def generate_test_data(self, num_samples: int = 50) -> list[dict]:
        """Generate a mix of valid solutions and random arrangements for testing."""
        rows_header = [f"Row_{i}" for i in range(self.n)]
        records: list[dict] = []

        # Include some real solutions
        real = random.sample(self.solutions, min(10, len(self.solutions)))
        for idx, sol in enumerate(real):
            sorted_sol = sorted(sol)
            record = {
                "ID": idx + 1,
                "Type": "Valid",
                "Positions": str(sorted_sol),
                "Expected_Valid": True,
            }
            for i in range(self.n):
                record[rows_header[i]] = sorted_sol[i][1]
            records.append(record)

        # Fill the rest with random (mostly invalid) arrangements
        base_id = len(records) + 1
        for k in range(num_samples - len(records)):
            cols = list(range(self.n))
            random.shuffle(cols)
            positions = [(row, cols[row]) for row in range(self.n)]
            valid, _ = self.is_valid(positions)
            record = {
                "ID": base_id + k,
                "Type": "Random",
                "Positions": str(positions),
                "Expected_Valid": valid,
            }
            for i in range(self.n):
                record[rows_header[i]] = positions[i][1]
            records.append(record)

        return records

    def save_test_data(
        self, filename: str = "queens_test_data.csv", num_samples: int = 50
    ) -> str:
        """Write test data to CSV and print a summary."""
        records = self.generate_test_data(num_samples)
        rows_header = [f"Row_{i}" for i in range(self.n)]
        fieldnames = ["ID", "Type"] + rows_header + ["Expected_Valid", "Positions"]

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

        valid_count = sum(1 for r in records if r["Expected_Valid"])
        print(f"Saved {len(records)} records to '{filename}'")
        print(f"  Valid: {valid_count}  |  Invalid: {len(records) - valid_count}")
        return filename

    def verify_csv(self, filename: str = "queens_test_data.csv") -> float:
        """Re-validate every row in the CSV and report accuracy."""
        print(f"\nVerifying '{filename}' ...")
        correct = total = 0

        with open(filename, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                positions = [(i, int(row[f"Row_{i}"])) for i in range(self.n)]
                valid, reason = self.is_valid(positions)
                expected = row["Expected_Valid"].lower() == "true"
                if valid == expected:
                    correct += 1
                else:
                    print(f"  ID {row['ID']}: expected {expected}, got {valid} ({reason})")
                total += 1

        accuracy = correct / total * 100
        print(f"Accuracy: {correct}/{total} = {accuracy:.1f}%")
        return accuracy


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    here = pathlib.Path(__file__).parent

    solver = NQueensSolver(8)
    solver.solve_all()
    print(f"Found {len(solver.solutions)} solutions to the 8-Queens problem.")

    csv_file = str(here / "queens_verification_data.csv")
    solver.save_test_data(csv_file, num_samples=100)
    solver.verify_csv(csv_file)

    for idx, out in enumerate(["nqueen_solution1.png", "nqueen_solution2.png"]):
        solver.visualize(idx, save=True, filename=str(here / out))
    print("Saved solution visualisations.")
