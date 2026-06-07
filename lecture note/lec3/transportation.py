"""
Transportation Problem — Gurobi implementation

A company ships PCs from three plants to four retail outlets.
Objective: minimise total shipping cost subject to supply and demand constraints.

  min  sum_{i in P, j in R}  c[i,j] * x[i,j]
  s.t. sum_{i in P} x[i,j] == demand[j]   for all j in R
       sum_{j in R} x[i,j] <= supply[i]   for all i in P
       x[i,j] >= 0
"""

from gurobipy import GRB, Model, quicksum

# ── Data ──────────────────────────────────────────────────────────────────────

plants = [1, 2, 3]
retailers = ["A", "B", "C", "D"]

supply = {1: 1700, 2: 2000, 3: 1700}
demand = {"A": 1700, "B": 1000, "C": 1500, "D": 1200}

cost_raw = [[5, 3, 2, 6], [7, 7, 8, 10], [6, 5, 3, 8]]
cost = {
    (plants[i], retailers[j]): cost_raw[i][j]
    for i in range(len(plants))
    for j in range(len(retailers))
}

# ── Model ─────────────────────────────────────────────────────────────────────

m = Model("transportation")
m.setParam("OutputFlag", 0)

x = m.addVars(plants, retailers, name="ship")

m.setObjective(x.prod(cost), GRB.MINIMIZE)

m.addConstrs(
    (x.sum("*", j) == demand[j] for j in retailers),
    name="demand",
)
m.addConstrs(
    (x.sum(i, "*") <= supply[i] for i in plants),
    name="supply",
)

# ── Solve ─────────────────────────────────────────────────────────────────────

m.optimize()

# ── Results ───────────────────────────────────────────────────────────────────

print(f"Optimal shipping cost: ${m.objVal:,.0f}")
print("\nShipment plan (plant → retailer : units):")
for (i, j), var in x.items():
    if var.x > 0:
        print(f"  Plant {i} → Retailer {j} : {var.x:.0f} units")
