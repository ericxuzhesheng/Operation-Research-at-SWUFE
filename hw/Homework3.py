import numpy as np
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB
import networkx as nx

# ----- data -----
# number of customers
n = 20

# generate locations
np.random.seed(0)
loc_x = np.random.randint(0, 100, n)
loc_y = np.random.randint(0, 100, n)

# generate scores
s = np.random.randint(1, 10, n)

# calculate travel time
c = {
    (i, j): ((loc_x[i] - loc_x[j]) ** 2 + (loc_y[i] - loc_y[j]) ** 2) ** 0.5
    for i in range(n)
    for j in range(n)
}

# time budget
T = 300

# Create model
m = gp.Model("Orienteering")

# Decision variables
# x[i,j] = 1 if we travel from node i to node j, 0 otherwise
x = m.addVars(c.keys(), vtype=GRB.BINARY, name="x")

# u[i] represents the position of node i in the tour (for subtour elimination)
u = m.addVars(range(1, n), lb=1, ub=n - 1, vtype=GRB.INTEGER, name="u")

# y[i] = 1 if node i is visited, 0 otherwise
y = m.addVars(range(n), vtype=GRB.BINARY, name="y")

# Objective: maximize the total collected score
m.setObjective(gp.quicksum(s[i] * y[i] for i in range(n)), GRB.MAXIMIZE)

# Constraints
# Node 0 must be the starting and ending point
m.addConstr(y[0] == 1, "visit_depot")

# Flow balance constraints
for j in range(n):
    m.addConstr(
        gp.quicksum(x[i, j] for i in range(n) if i != j) == y[j], f"in_flow_{j}"
    )
    m.addConstr(
        gp.quicksum(x[j, i] for i in range(n) if i != j) == y[j], f"out_flow_{j}"
    )

# Time budget constraint
m.addConstr(
    gp.quicksum(c[i, j] * x[i, j] for i, j in c.keys() if i != j) <= T, "time_budget"
)

# Miller-Tucker-Zemlin subtour elimination constraints
for i in range(1, n):
    for j in range(1, n):
        if i != j:
            m.addConstr(u[i] - u[j] + n * x[i, j] <= n - 1, f"mtz_{i}_{j}")

# Solve the model
m.optimize()

# Extract solution
if m.status == GRB.OPTIMAL:
    tour = []
    current = 0  # Start from depot
    tour.append(current)

    while True:
        for j in range(n):
            if j != current and x[current, j].x > 0.5:
                tour.append(j)
                current = j
                break
        if current == 0 and len(tour) > 1:
            break

    # Calculate total collected score and total travel time
    total_score = sum(s[i] for i in tour)
    total_time = sum(c[tour[i], tour[i + 1]] for i in range(len(tour) - 1))

    print(f"Optimal tour: {tour}")
    print(f"Total collected score: {total_score}")
    print(f"Total travel time: {total_time:.2f}")

    # Plot the solution
    plt.figure(figsize=(10, 8))

    # Plot all nodes
    plt.scatter(loc_x, loc_y, s=100, c="lightgray", edgecolors="black", zorder=1)

    # Plot visited nodes
    visited_nodes = [i for i in range(n) if y[i].x > 0.5]
    plt.scatter(
        loc_x[visited_nodes],
        loc_y[visited_nodes],
        s=100,
        c="green",
        edgecolors="black",
        zorder=2,
    )

    # Highlight depot
    plt.scatter(
        loc_x[0], loc_y[0], s=150, c="red", edgecolors="black", marker="*", zorder=3
    )

    # Plot edges
    for i in range(len(tour) - 1):
        plt.plot(
            [loc_x[tour[i]], loc_x[tour[i + 1]]],
            [loc_y[tour[i]], loc_y[tour[i + 1]]],
            "b-",
            zorder=1,
        )

    # Add node labels
    for i in range(n):
        plt.annotate(
            f"{i}\n(s={s[i]})",
            (loc_x[i], loc_y[i]),
            textcoords="offset points",
            xytext=(0, 5),
            ha="center",
        )

    plt.title(
        f"Orienteering Solution\nTotal Score: {total_score}, Travel Time: {total_time:.2f}"
    )
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(r"d:\Visual Studio Code\Operation Research\orienteering_solution.jpg")
    plt.show()
else:
    print("No solution found.")
