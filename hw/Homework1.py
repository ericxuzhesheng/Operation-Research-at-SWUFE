"""
Homework 1 — Mean-Variance Portfolio Optimization

Finds the minimum-risk portfolio that achieves a target expected return β,
using the Charnes-Cooper transformation to convert the fractional programme
into a tractable QP.

Model (after transformation, letting x̄ = x·z):
  min   x̄' Σ x̄
  s.t.  1' x̄  ≤ B·z          (budget)
        μ' x̄  − β·z = 1      (target return)
        x̄ ≥ 0,  z ≥ 0
"""

import pathlib

import gurobipy as gp
import numpy as np
import pandas as pd
from gurobipy import GRB

# ── Data ──────────────────────────────────────────────────────────────────────

data_file = pathlib.Path(__file__).parent / "../lecture note/lec3/data_portfolio.csv"
data = pd.read_csv(data_file)
stocks = data.columns.values

mu = data.mean()
sigma = data.cov()

BUDGET = 1000
TARGET_RETURN = 5

# ── Model ─────────────────────────────────────────────────────────────────────

m = gp.Model("portfolio_min_variance")
m.setParam("OutputFlag", 0)

x_bar = m.addVars(stocks, name="x_bar")
z = m.addVar(name="z", lb=0)

# Objective: minimise portfolio variance  x̄' Σ x̄
obj = gp.quicksum(
    sigma.loc[i, j] * x_bar[i] * x_bar[j]
    for i in stocks
    for j in stocks
)
m.setObjective(obj, GRB.MINIMIZE)

m.addConstr(gp.quicksum(x_bar[s] for s in stocks) <= BUDGET * z, name="budget")
m.addConstr(
    gp.quicksum(mu[s] * x_bar[s] for s in stocks) - TARGET_RETURN * z == 1,
    name="return",
)
m.addConstrs((x_bar[s] >= 0 for s in stocks), name="nonneg")

# ── Solve ─────────────────────────────────────────────────────────────────────

m.optimize()

# ── Results ───────────────────────────────────────────────────────────────────

if m.status == GRB.OPTIMAL:
    z_val = z.x
    weights = {s: x_bar[s].x / z_val for s in stocks if x_bar[s].x / z_val > 1e-6}

    print("Optimal Portfolio:")
    for stock, w in weights.items():
        print(f"  {stock}: {w:.4f}")

    w_arr = np.array([weights.get(s, 0.0) for s in stocks])
    exp_return = float(np.dot(mu, w_arr))
    risk = float(np.sqrt(w_arr @ sigma.values @ w_arr))

    print(f"\nExpected return : {exp_return:.4f}")
    print(f"Risk (std dev)  : {risk:.4f}")
    print(f"Sharpe ratio    : {(exp_return - TARGET_RETURN) / risk:.4f}")
    print(f"Total investment: {sum(weights.values()):.2f}")
else:
    print("No optimal solution found.")
