import gurobipy as gp
from gurobipy import GRB
import numpy as np

# Define the revenue data for each store ($1000s)
revenues = {1: 127, 2: 83, 3: 165, 4: 96, 5: 112, 6: 88, 7: 135, 8: 141, 9: 117, 10: 94}

# Create a model
model = gp.Model("Grocery_Store_Optimization")

# Create binary decision variables for each store
# x[i] = 1 if store i is kept open, 0 otherwise
x = model.addVars(revenues.keys(), vtype=GRB.BINARY, name="x")

# Set objective: maximize total revenue
model.setObjective(
    gp.quicksum(revenues[i] * x[i] for i in revenues.keys()), GRB.MAXIMIZE
)

# Define the proximity sets (stores within 2 miles of each other)
proximity_sets = [
    [1, 2, 4],
    [1, 3],
    [4, 5, 6],
    [6, 7, 8],
    [6, 9],
    [8, 10],
    [9, 10],
]

# Add constraints: at most one store in each proximity set can be open
for i, proximity_set in enumerate(proximity_sets):
    model.addConstr(
        gp.quicksum(x[j] for j in proximity_set) <= 1, f"proximity_set_{i+1}"
    )

# Optimize the model
model.optimize()

# Print results
if model.status == GRB.OPTIMAL:
    print(f"Optimal solution found with total revenue: ${model.objVal:.0f}k")
    print("\nStores to keep open:")
    total_revenue = 0
    open_stores = []
    for i in revenues.keys():
        if x[i].x > 0.5:  # If the store is open (allowing for small numerical errors)
            print(f"Store {i}: ${revenues[i]}k")
            total_revenue += revenues[i]
            open_stores.append(i)
    print(f"\nTotal revenue: ${total_revenue}k")
    print(f"Open stores: {open_stores}")
else:
    print("No optimal solution found.")

# Verify the solution by checking constraints
print("\nVerifying solution:")
for i, proximity_set in enumerate(proximity_sets):
    open_in_set = sum(1 for j in proximity_set if x[j].x > 0.5)
    if open_in_set > 1:
        print(
            f"ERROR: More than one store is open in proximity set {i+1}: {proximity_set}"
        )
    else:
        print(f"Constraint for proximity set {i+1} {proximity_set} is satisfied.")

# Calculate how many stores are kept open
stores_kept_open = sum(1 for i in revenues.keys() if x[i].x > 0.5)
print(f"\nTotal stores kept open: {stores_kept_open} out of 10")
