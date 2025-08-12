import pandas as pd
import numpy as np
from gurobipy import *

# Data loading and preprocessing
data = pd.read_csv(r"d:\Visual Studio Code\Operation Research\data_portfolio.csv")
stocks = data.columns.values

# Calculate mean returns and covariance matrix
mu = data.mean()
Sigma = data.cov()

# Set parameters
B = 1000  # budget
beta = 5  # target return

# Create model
m = Model("portfolio_prob_max")

# Add variables
x_bar = m.addVars(stocks, name="x_bar")
z = m.addVar(name="z")

# Set objective: minimize x'Σx
obj = quicksum(Sigma.loc[i, j] * x_bar[i] * x_bar[j] for i in stocks for j in stocks)
m.setObjective(obj, GRB.MINIMIZE)

# Add constraints
# Budget constraint: 1'x_bar ≤ Bz
m.addConstr(quicksum(x_bar[s] for s in stocks) <= B * z, name="budget")

# Expected return constraint: μ'x_bar - βz = 1
m.addConstr(quicksum(mu[s] * x_bar[s] for s in stocks) - beta * z == 1, name="return")

# Non-negativity constraints
m.addConstr(z >= 0, name="z_nonneg")
for s in stocks:
    m.addConstr(x_bar[s] >= 0, name=f"x_{s}_nonneg")

# Solve model
m.optimize()

# Output results
if m.status == GRB.OPTIMAL:
    print("\nOptimal Solution:")
    # Calculate actual portfolio weights x = x_bar/z
    z_val = z.x
    portfolio = {}
    for s in stocks:
        x_val = x_bar[s].x / z_val
        if x_val > 1e-6:  # Only print significant investments
            portfolio[s] = x_val
            print(f"{s}: {x_val:.4f}")

    # Calculate portfolio statistics
    weights = np.array([portfolio.get(s, 0) for s in stocks])
    exp_return = np.dot(mu, weights)
    risk = np.sqrt(np.dot(weights.T, np.dot(Sigma, weights)))

    print(f"\nPortfolio Statistics:")
    print(f"Total Investment: {sum(portfolio.values()):.2f}")
    print(f"Expected Return: {exp_return:.4f}")
    print(f"Risk (Std Dev): {risk:.4f}")
    print(f"Sharpe Ratio: {(exp_return - beta)/risk:.4f}")
else:
    print("Model optimization failed")
