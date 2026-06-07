"""
Fixed-Charge Facility Location (FCFL) — data preparation

Reads Chinese city data from cn.csv, filters to provincial capitals,
and constructs the sets and parameters used by the FCFL model in lec4.ipynb.

Parameters
----------
I  : set of demand nodes (cities / customers)
J  : set of candidate facility locations (same as I here)
d  : demand at each node (scaled population)
f  : fixed opening cost for each facility
v  : variable (per-unit) service cost for each facility
c  : travel cost matrix between every (i, j) pair (Euclidean distance)
"""

import pathlib

import gurobipy as gp
import numpy as np
import pandas as pd

# ── Load and filter city data ─────────────────────────────────────────────────

data_file = pathlib.Path(__file__).parent / "cn.csv"
data = pd.read_csv(data_file)
data = data[data["capital"].isin(["admin", "primary"])]

n = len(data)
cities = data["city"].values
loc_x = dict(zip(cities, data["lat"].values))
loc_y = dict(zip(cities, data["lng"].values))

# ── Sets ──────────────────────────────────────────────────────────────────────

I = cities   # demand nodes
J = cities   # candidate facility locations

# ── Parameters ────────────────────────────────────────────────────────────────

d = dict(zip(cities, data["population"].values * 1e-5))   # scaled demand
f = {j: 1e3 for j in J}                                   # fixed cost
v = {j: 3e2 for j in J}                                   # variable cost

# Euclidean distance (degree-based approximation)
c = {
    (i, j): ((loc_x[i] - loc_x[j]) ** 2 + (loc_y[i] - loc_y[j]) ** 2) ** 0.5
    for i in I
    for j in J
}

print(f"Loaded {n} cities.")
print(f"Demand range : {min(d.values()):.2f} – {max(d.values()):.2f}")
print(f"Distance range: {min(c.values()):.2f} – {max(c.values()):.2f}")
print("Data ready for FCFL model (see lec4.ipynb).")
