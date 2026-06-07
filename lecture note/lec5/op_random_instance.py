"""
Orienteering Problem — random instance generator and MIP solver

Orienteering: start and end at a depot, collect as many score points as
possible while staying within a travel-time budget T.

Model:
  - Binary x[i,j]: 1 if we travel from node i to node j
  - Binary y[i]: 1 if node i is visited
  - Integer u[i]: position of node i in the tour (MTZ subtour elimination)
  - Objective: maximise sum of scores of visited nodes
"""

import pathlib

import gurobipy as gp
import matplotlib.pyplot as plt
import numpy as np

# ── Instance parameters ───────────────────────────────────────────────────────

N_CUSTOMERS = 20
TIME_BUDGET = 300
SEED = 0

# ── Generate random instance ──────────────────────────────────────────────────

rng = np.random.default_rng(SEED)
n = N_CUSTOMERS
loc_x = rng.integers(0, 100, n)
loc_y = rng.integers(0, 100, n)
scores = rng.integers(1, 10, n)

travel_time = {
    (i, j): ((loc_x[i] - loc_x[j]) ** 2 + (loc_y[i] - loc_y[j]) ** 2) ** 0.5
    for i in range(n)
    for j in range(n)
}

# ── Model ─────────────────────────────────────────────────────────────────────

mdl = gp.Model("orienteering")

x = mdl.addVars(travel_time.keys(), vtype=gp.GRB.BINARY, name="x")
y = mdl.addVars(range(n), vtype=gp.GRB.BINARY, name="y")
u = mdl.addVars(range(1, n), lb=1, ub=n - 1, vtype=gp.GRB.INTEGER, name="u")

# Maximise total collected score
mdl.setObjective(gp.quicksum(scores[i] * y[i] for i in range(n)), gp.GRB.MAXIMIZE)

# Depot must be visited
mdl.addConstr(y[0] == 1, name="depot")

# Flow balance: in-flow == out-flow == visit indicator
for j in range(n):
    mdl.addConstr(
        gp.quicksum(x[i, j] for i in range(n) if i != j) == y[j],
        name=f"in_{j}",
    )
    mdl.addConstr(
        gp.quicksum(x[j, i] for i in range(n) if i != j) == y[j],
        name=f"out_{j}",
    )

# Time budget
mdl.addConstr(
    gp.quicksum(travel_time[i, j] * x[i, j] for i, j in travel_time if i != j)
    <= TIME_BUDGET,
    name="budget",
)

# MTZ subtour elimination
for i in range(1, n):
    for j in range(1, n):
        if i != j:
            mdl.addConstr(u[i] - u[j] + n * x[i, j] <= n - 1, name=f"mtz_{i}_{j}")

# ── Solve ─────────────────────────────────────────────────────────────────────

mdl.optimize()

# ── Results ───────────────────────────────────────────────────────────────────

if mdl.status == gp.GRB.OPTIMAL:
    # Reconstruct tour
    tour = [0]
    current = 0
    while True:
        for j in range(n):
            if j != current and x[current, j].x > 0.5:
                tour.append(j)
                current = j
                break
        if current == 0 and len(tour) > 1:
            break

    total_score = sum(scores[i] for i in tour)
    total_time = sum(
        travel_time[tour[i], tour[i + 1]] for i in range(len(tour) - 1)
    )

    print(f"Optimal tour   : {tour}")
    print(f"Total score    : {total_score}")
    print(f"Total time     : {total_time:.2f} / {TIME_BUDGET}")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(loc_x, loc_y, s=80, c="lightgray", edgecolors="black", zorder=1)

    visited = [i for i in range(n) if y[i].x > 0.5]
    ax.scatter(
        loc_x[visited], loc_y[visited], s=80, c="green", edgecolors="black", zorder=2
    )
    ax.scatter(loc_x[0], loc_y[0], s=150, c="red", marker="*", zorder=3)

    for i in range(len(tour) - 1):
        ax.plot(
            [loc_x[tour[i]], loc_x[tour[i + 1]]],
            [loc_y[tour[i]], loc_y[tour[i + 1]]],
            "b-",
            zorder=1,
        )

    for i in range(n):
        ax.annotate(
            f"{i}\n(s={scores[i]})",
            (loc_x[i], loc_y[i]),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=7,
        )

    ax.set_title(
        f"Orienteering — Score: {total_score}, Time: {total_time:.1f}/{TIME_BUDGET}"
    )
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    plt.tight_layout()
    out = pathlib.Path(__file__).parent / "orienteering_solution.jpg"
    plt.savefig(out)
    print(f"Plot saved to '{out}'.")
else:
    print("No optimal solution found.")
