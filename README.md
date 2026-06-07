# 西南财经大学运筹学 | Operations Research at SWUFE

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Gurobi-11%2B-ED1C24?style=flat-square" alt="Gurobi" />
  <img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat-square&logo=jupyter&logoColor=white" alt="Jupyter" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License" />
</p>

<p align="center">
  <a href="#chinese">中文</a> · <a href="#english">English</a>
</p>

---

<a id="chinese"></a>

## 概览

本仓库汇集了**西南财经大学运筹学课程**的完整学习资料，涵盖七个渐进式讲座模块的理论基础与 Python/Gurobi 实践实现。

## 仓库结构

```
.
├── slide/
│   ├── theory/          # 理论讲义（线性规划、整数规划、图与网络）
│   └── practice/        # 实践讲义（Python、Gurobi、案例研究）
├── lecture note/
│   ├── lec2/            # 线性规划基础（Gurobi 入门）
│   ├── lec3/            # 投资组合优化与运输问题
│   ├── lec4/            # 设施选址（p-中位数、固定成本设施选址）
│   ├── lec5/            # 旅行商问题与定向越野问题
│   ├── lec6/            # 启发式方法——模拟退火
│   └── lec7/            # 数独求解（约束规划）
├── hw/
│   ├── Homework1.py     # 投资组合优化（均值-方差模型）
│   ├── Homework2.py     # 超市选址二进制整数规划
│   └── Homework3.py     # 定向越野问题（TSP 变体）
└── final/
    └── submission/      # N 皇后问题——期末项目
```

## 课程模块

| # | 主题 | 讲义 | Notebook | 代码 |
|---|------|------|----------|------|
| 1 | Python 入门 | [PDF](slide/practice/1-Intro%20to%20Python.pdf) | — | — |
| 2 | Gurobi 实战 · 线性规划 | [PDF](slide/practice/2-Hands-on%20Gurobi.pdf) | [lec2.ipynb](lecture%20note/lec2/lec2.ipynb) | — |
| 3 | 投资组合优化 · 运输问题 | [PDF](slide/practice/3-Portfolio%20Optimization.pdf) | [lec3.ipynb](lecture%20note/lec3/lec3.ipynb) | [transportation.py](lecture%20note/lec3/transportation.py) |
| 4 | 设施选址（p-中位数、FCFL）| [PDF](slide/practice/4-Facility%20Location.pdf) | [lec4.ipynb](lecture%20note/lec4/lec4.ipynb) | [fcfl-data.py](lecture%20note/lec4/fcfl-data.py) |
| 5 | 旅行商问题（TSP）| [PDF](slide/practice/5-Traveling%20Salesman%20Problem.pdf) | [lec5.ipynb](lecture%20note/lec5/lec5.ipynb) | [cvrp.py](lecture%20note/lec5/cvrp.py) |
| 6 | 启发式与元启发式算法 | [PDF](slide/practice/6-Heuristics.pdf) | [lec6.ipynb](lecture%20note/lec6/lec6.ipynb) | [SA.py](lecture%20note/lec6/SA.py) |
| 7 | 数独求解 | [PDF](slide/practice/7-Sudoku.pdf) | [lec7.ipynb](lecture%20note/lec7/lec7.ipynb) | — |

**理论讲义：** [线性规划](slide/theory/PPT1-Introduction%20and%20linear%20programming.pdf) · [整数规划](slide/theory/PPT2-Integer%20prgramming.pdf) · [图与网络](slide/theory/PPT3-Graph%20and%20network.pdf)

## 环境要求

- Python 3.10+
- 有效的 [Gurobi 许可证](https://www.gurobi.com/academia/academic-program-and-licenses/)（学生和学术用户免费）

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/ericxuzhesheng/Operation-Research-at-SWUFE.git
cd Operation-Research-at-SWUFE

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动 Jupyter 浏览讲义 Notebook
jupyter lab "lecture note/"
```

## 作业说明

| 文件 | 问题 | 方法 |
|------|------|------|
| [Homework1.py](hw/Homework1.py) | 均值-方差投资组合优化 | 二次规划（Gurobi）|
| [Homework2.py](hw/Homework2.py) | 超市营收最大化 | 二进制整数规划 |
| [Homework3.py](hw/Homework3.py) | 定向越野问题（得分收集型 TSP）| MTZ 子回路消除的混合整数规划 |

## 期末项目

**N 皇后问题** — 使用 Gurobi 的 MIP 求解器配合惰性约束，枚举 N 皇后问题的所有解。

- [源代码](final/submission/N-Queen%20puzzle.py)
- [报告（PDF）](final/submission/N_Queens_puzzle.pdf)
- [验证数据（CSV）](final/submission/queens_verification_data.csv)

---

<a id="english"></a>

## Overview

Course materials for the **Operations Research** course at [Southwestern University of Finance and Economics (SWUFE)](https://www.swufe.edu.cn/). The repository covers both theory and hands-on Python/Gurobi implementation across seven progressive lecture modules.

## Repository Structure

```
.
├── slide/
│   ├── theory/          # Theoretical lecture slides (LP, IP, Graph & Network)
│   └── practice/        # Hands-on practice slides (Python, Gurobi, case studies)
├── lecture note/
│   ├── lec2/            # Linear programming basics (Gurobi intro)
│   ├── lec3/            # Portfolio optimization & transportation
│   ├── lec4/            # Facility location (p-median, FCFL)
│   ├── lec5/            # Traveling salesman & orienteering
│   ├── lec6/            # Heuristics — simulated annealing
│   └── lec7/            # Sudoku solver (constraint programming)
├── hw/
│   ├── Homework1.py     # Portfolio optimization (mean-variance model)
│   ├── Homework2.py     # Grocery store binary IP
│   └── Homework3.py     # Orienteering problem (TSP variant)
└── final/
    └── submission/      # N-Queens puzzle — final project
```

## Course Modules

| # | Topic | Slides | Notebook | Code |
|---|-------|--------|----------|------|
| 1 | Intro to Python | [PDF](slide/practice/1-Intro%20to%20Python.pdf) | — | — |
| 2 | Hands-on Gurobi · Linear Programming | [PDF](slide/practice/2-Hands-on%20Gurobi.pdf) | [lec2.ipynb](lecture%20note/lec2/lec2.ipynb) | — |
| 3 | Portfolio Optimization · Transportation | [PDF](slide/practice/3-Portfolio%20Optimization.pdf) | [lec3.ipynb](lecture%20note/lec3/lec3.ipynb) | [transportation.py](lecture%20note/lec3/transportation.py) |
| 4 | Facility Location (p-Median, FCFL) | [PDF](slide/practice/4-Facility%20Location.pdf) | [lec4.ipynb](lecture%20note/lec4/lec4.ipynb) | [fcfl-data.py](lecture%20note/lec4/fcfl-data.py) |
| 5 | Traveling Salesman Problem (TSP) | [PDF](slide/practice/5-Traveling%20Salesman%20Problem.pdf) | [lec5.ipynb](lecture%20note/lec5/lec5.ipynb) | [cvrp.py](lecture%20note/lec5/cvrp.py) |
| 6 | Heuristics & Metaheuristics | [PDF](slide/practice/6-Heuristics.pdf) | [lec6.ipynb](lecture%20note/lec6/lec6.ipynb) | [SA.py](lecture%20note/lec6/SA.py) |
| 7 | Sudoku Solver | [PDF](slide/practice/7-Sudoku.pdf) | [lec7.ipynb](lecture%20note/lec7/lec7.ipynb) | — |

**Theory slides:** [Linear Programming](slide/theory/PPT1-Introduction%20and%20linear%20programming.pdf) · [Integer Programming](slide/theory/PPT2-Integer%20prgramming.pdf) · [Graph & Network](slide/theory/PPT3-Graph%20and%20network.pdf)

## Prerequisites

- Python 3.10+
- A valid [Gurobi license](https://www.gurobi.com/academia/academic-program-and-licenses/) (free for students and academics)

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/ericxuzhesheng/Operation-Research-at-SWUFE.git
cd Operation-Research-at-SWUFE

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Jupyter to explore lecture notebooks
jupyter lab "lecture note/"
```

## Homework Summary

| File | Problem | Method |
|------|---------|--------|
| [Homework1.py](hw/Homework1.py) | Mean-variance portfolio optimization | Quadratic programming (Gurobi) |
| [Homework2.py](hw/Homework2.py) | Grocery store revenue maximization | Binary integer programming |
| [Homework3.py](hw/Homework3.py) | Orienteering problem (score-collecting TSP) | MIP with MTZ subtour elimination |

## Final Project

**N-Queens Puzzle** — solve the classic N-Queens problem using Gurobi's MIP solver with lazy constraints to enumerate all solutions.

- [Source code](final/submission/N-Queen%20puzzle.py)
- [Report (PDF)](final/submission/N_Queens_puzzle.pdf)
- [Verification data (CSV)](final/submission/queens_verification_data.csv)

---

## 许可证 | License

本项目基于 [MIT 许可证](LICENSE) 开源。  
Released under the [MIT License](LICENSE).
