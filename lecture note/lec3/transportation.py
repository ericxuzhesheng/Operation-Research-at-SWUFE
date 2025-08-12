# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 14:29:25 2025

@author: lab
"""

from gurobipy import *


# data
plant = [1, 2, 3]
retailer = ["A", "B", "C", "D"]
capacity_raw = [1700, 2000, 1700]
# capacity = {plant[i]:capacity_raw[i] for i in range(len(plant))}
capacity = dict(zip(plant, capacity_raw))
demand_raw = [1700, 1000, 1500, 1200]
demand = dict(zip(retailer, demand_raw))
cost_raw = [[5, 3, 2, 6], [7, 7, 8, 10], [6, 5, 3, 8]]
cost = {
    (plant[i], retailer[j]): cost_raw[i][j]
    for i in range(len(plant))
    for j in range(len(retailer))
}

# model

m = Model("transportation")

# 1. decision variables
x = m.addVars(plant, retailer, name="transport_qty")

# 2. objective
m.setObjective(x.prod(cost), sense=GRB.MINIMIZE)

# 3. constraints
m.addConstrs((x.sum("*", j) == demand[j] for j in retailer), name="retailer_con")
m.addConstrs((x.sum(i, "*") <= capacity[i] for i in plant), name="plant_con")


m.optimize()

# analysis
for v in m.getVars():
    print(v.varName, "=", v.x)
print("obj val =", m.objVal)
