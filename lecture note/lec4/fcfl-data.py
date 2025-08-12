import numpy as np
import pandas as pd
import gurobipy as gp
import folium

# ----- data ------
# read data for all cities
data = pd.read_csv('cn.csv')
# only captials
data = data[(data['capital'] == 'admin') | (data['capital'] == 'primary')]

# parameters
n = data.shape[0]
loc_x_vals = data['lat'].values
loc_y_vals = data['lng'].values
pop_vals = data['population'].values
cities = data['city'].values
loc_x = dict(zip(cities, loc_x_vals))
loc_y = dict(zip(cities, loc_y_vals))

I = cities
J = cities
d = dict(zip(cities, pop_vals * 1e-5))
f = {j:1e3 for j in J}
v = {j:3e2 for j in J}

# calculate distance
c = {(i,j):((loc_x[i] - loc_x[j])**2 + (loc_y[i] - loc_y[j])**2)**.5 
     for i in I for j in J}
