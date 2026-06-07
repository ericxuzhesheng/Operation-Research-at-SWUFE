"""
Capacitated Vehicle Routing Problem with Time Windows (CVRPTW)

Data: Solomon benchmark instance r102 (first 20 customers + depot).

Model:
  - Binary variable x[i,j]: 1 if a vehicle travels directly from i to j
  - Continuous variable u[i]: cumulative load when leaving node i
  - Objective: minimise total travel distance
  - Constraints: flow balance, vehicle count, capacity via indicator constraints
"""

import pathlib

import gurobipy as gp
import matplotlib.pyplot as plt

# ── Data ──────────────────────────────────────────────────────────────────────

n = 20                          # number of customers
Nc = list(range(1, n + 1))     # customer nodes
N = list(range(n + 1))         # all nodes (depot = 0)
A = [(i, j) for i in N for j in N if i != j]

cx, cy, q, e, l, s = [], [], [], [], [], []

data_file = pathlib.Path(__file__).parent / "r102.txt"
with open(data_file) as f:
    for _ in range(4):          # skip header lines
        f.readline()
    vals = f.readline().split()
    m = int(vals[0])            # number of vehicles
    Q = int(vals[1])            # vehicle capacity
    for _ in range(4):
        f.readline()
    for _ in N:
        row = f.readline().split()
        cx.append(int(row[1]))
        cy.append(int(row[2]))
        q.append(int(row[3]))
        e.append(int(row[4]))
        l.append(int(row[5]))
        s.append(int(row[6]))

c = {
    (i, j): round(((cx[i] - cx[j]) ** 2 + (cy[i] - cy[j]) ** 2) ** 0.5, 2)
    for i, j in A
}

# ── Model ─────────────────────────────────────────────────────────────────────

mdl = gp.Model("cvrptw")
mdl.params.timelimit = 30

x = mdl.addVars(A, vtype=gp.GRB.BINARY, name="x")
u = mdl.addVars(N, lb=q, ub=Q, name="u")

mdl.setObjective(x.prod(c), sense=gp.GRB.MINIMIZE)

# Each customer visited exactly once
mdl.addConstrs((x.sum("*", i) == 1 for i in Nc), name="inflow")
mdl.addConstrs((x.sum(i, "*") == 1 for i in Nc), name="outflow")

# Fleet size limit
mdl.addConstr(x.sum(0, "*") <= m, name="vehicles")

# Capacity & subtour elimination (indicator form)
mdl.addConstrs(
    (x[i, j] == 1) >> (u[j] >= u[i] + q[j])
    for i in Nc
    for j in Nc
    if i != j
)

# ── Solve ─────────────────────────────────────────────────────────────────────

mdl.optimize()

# ── Results ───────────────────────────────────────────────────────────────────

print(f"Optimality gap: {mdl.mipgap:.4%}")

if mdl.status != gp.GRB.INFEASIBLE:
    fig, ax = plt.subplots()
    ax.scatter(cx[0], cy[0], c="red", marker="s", label="Depot")
    ax.scatter(cx[1:], cy[1:], label="Customer")

    for i, j in A:
        if x[i, j].x > 0.9:
            ax.plot([cx[i], cx[j]], [cy[i], cy[j]], "g-", linewidth=0.8)

    ax.legend()
    ax.set_title("CVRPTW Solution")
    output = pathlib.Path(__file__).parent / "vrp.png"
    plt.savefig(output, dpi=300)
    print(f"Route plot saved to '{output}'.")
