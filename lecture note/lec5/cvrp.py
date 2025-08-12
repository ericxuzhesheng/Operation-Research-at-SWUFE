import matplotlib.pyplot as plt
import gurobipy as gp

# data
n = 20
Nc = list(range(1, n + 1))
N = list(range(n + 1))
A = [(i,j) for i in N for j in N if i != j]
cx = []
cy = []
q = []
e = []
l = []
s = []
with open('r102.txt') as f:
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    vals = f.readline().split()
    m = int(vals[0])
    Q = int(vals[1])
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    for i in N:
        vals = f.readline().split()
        cx.append(int(vals[1]))
        cy.append(int(vals[2]))
        q.append(int(vals[3]))
        e.append(int(vals[4]))
        l.append(int(vals[5]))
        s.append(int(vals[6]))

c = {(i,j):round(((cx[i] - cx[j])**2 + (cy[i] - cy[j])**2)**.5, 2) for i,j in A}

# model
mdl = gp.Model('vrp')

# decision variables
x = mdl.addVars(A, vtype=gp.GRB.BINARY, name='x')
u = mdl.addVars(N, lb=q, ub=Q, name='u')    # define u[0] but do not use, for ease to define its lb and ub

# objective function
mdl.setObjective(x.prod(c), sense=gp.GRB.MINIMIZE)

# constraints: flow conservation
mdl.addConstrs((x.sum('*', i) == 1 for i in Nc), name='inflow')
mdl.addConstrs((x.sum(i, '*') == 1 for i in Nc), name='outflow')
mdl.addConstr(x.sum(0, '*') <= m, name='vehicle')

# constraints: capacity & subtour elimination
mdl.addConstrs(((x[i,j] == 1) >> (u[j] >= u[i] + q[j])
                for i in Nc for j in Nc if i != j), name='capacity')

# optimize
mdl.write('cvrp.lp')
mdl.params.timelimit = 30
mdl.optimize()

# print soluiton
print('the optimality gap =', mdl.mipgap)
if mdl.status != gp.GRB.INFEASIBLE:
    plt.scatter(cx[0], cy[0], c='r', marker='s')  # the depot
    plt.scatter(cx[1:], cy[1:])
    selected = [(i,j) for (i,j) in A if x[i,j].x > .9]
    for (i,j) in selected:
        plt.plot((cx[i], cx[j]), (cy[i], cy[j]), c='g')
    plt.savefig('vrp.png', dpi=300)
