import numpy as np
import matplotlib.pyplot as plt
import gurobipy as gp

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
