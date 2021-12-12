from ortools.linear_solver import pywraplp
import os

os.chdir('data')

def create_data_model(filename):
    data = {}
    with open(filename, 'r') as f:
        data['N'], data['K'] = [int(x) for x in f.readline().split()]
        data['d'] = [int(x) for x in f.readline().split()[:data['N']]]
        data['t'] = []  
        for _ in range(data['N'] + 1):
            data['t'].append([int(x) for x in f.readline().split()[:data['N']+1]])
    return data

data = create_data_model('N6-K2.txt')
print(data)

solver = pywraplp.Solver.CreateSolver('CBC')
INF = solver.infinity()

total_fix_time = sum(data['d'])
total_travel_time = sum(sum(i) for i in data['t'])

x = [[[solver.IntVar(0, 1, f'x({u}, {i}, {j})') for j in range(data['N']+1)] for i in range(data['N']+1)] for u in range(data['K'])]
y = [solver.IntVar(0, total_fix_time, f'y({u})') for u in range(data['K'])]
z = [solver.IntVar(0, total_fix_time + total_travel_time, f'z({u})') for u in range(data['K'])]
w = solver.IntVar(0, total_fix_time + total_travel_time, 'w')

for i in range(1, data['N']+1):
    c1 = solver.Constraint(1, 1)
    for k in range(data['K']):
        for j in range(data['N']+1):
            if j != i:
                c1.SetCoefficient(x[k][i][j], 1)

for j in range(1, data['N']+1):
    c2 = solver.Constraint(1, 1)
    for k in range(data['K']):
        for i in range(data['N']+1):
            if i != j:
                c2.SetCoefficient(x[k][i][j], 1)

for k in range(data['K']):
    for l in range(data['N']+1):
        c3 = solver.Constraint(0, 0)
        for i in range(data['N']+1):
            if i != l:
                c3.SetCoefficient(x[k][i][l], 1)
        for j in range(data['N']+1):
            if j != l:
                c3.SetCoefficient(x[k][l][j], -1)

for k in range(data['K']):
    c4 = solver.Constraint(1, 1)
    for j in range(1, data['N']+1):
        c4.SetCoefficient(x[k][0][j], 1)

for k in range(data['K']):
    c5 = solver.Constraint(1, 1)
    for i in range(1, data['N']+1):
        c5.SetCoefficient(x[k][i][0], 1)

for k in range(data['K']):
    c6 = solver.Constraint(0, 0)
    c6.SetCoefficient(y[k], -1)
    for i in range(data['N']+1):
        for j in range(1, data['N']+1):
            if i != j:
                c6.SetCoefficient(x[k][i][j], data['d'][j-1])

for k in range(data['K']):
    c7 = solver.Constraint(0, 0)
    c7.SetCoefficient(z[k], -1)
    c7.SetCoefficient(y[k], 1)
    for i in range(data['N']+1):
        for j in range(1, data['N']+1):
            if i != j:
                c7.SetCoefficient(x[k][i][j], data['t'][i][j])

for k in range(data['K']):
    c8 = solver.Constraint(0, INF)
    c8.SetCoefficient(z[k], -1)
    c8.SetCoefficient(w, 1)

# Objective
obj = solver.Objective()
obj.SetCoefficient(w, 1)
obj.SetMinimization()

rs = solver.Solve()

print(f'Optimal objective value: {obj.Value()}')
res = [[[x[u][i][j].solution_value() for j in range(data['N']+1)] for i in range(data['N']+1)] for u in range(data['K'])]

def print_schedule(res):
    for k in range(data['K']):
        print(f'Schedule of {k+1}:')
        for i in range(data['N']+1):
            for j in range(data['N']+1):
                if res[k][i][j] == 1:
                    print(f'{i} -> {j}')

print_schedule(res)