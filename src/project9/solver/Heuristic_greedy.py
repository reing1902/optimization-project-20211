import numpy as np

def create_data(filename):
    with open(filename) as f:
        N, K = [int(x) for x in f.readline().split()]
        d = [int(x) for x in f.readline().split()]
        t = [[int(x) for x in f.readline().split()] for i in range(N+1)]
    return N, K, d, t

filename = input("data file's name: ")
N, K, d, t = create_data(filename)


x = np.array([0 for k in range(K)]) #working time of staff k
y = {k:[0] for k in range(K)} #customers that staff k serves

customers = [n for n in range(1, N+1)]
while len(customers) != 0:
    staff = np.argmin(x)
    i = y[staff][-1]
    knowledge = []
    for l in customers:
        knowledge.append((l, t[i][l] + d[l-1]))
    knowledge.sort(key = lambda item: item[1])
    j = knowledge[0][0]
    y[staff].append(j)
    x[staff] += knowledge[0][1]
    customers.remove(j)
for k in range(K):
    x[k] += t[y[k][-1]][0]
    y[k].append(0)

print(f'Optimal cost: {np.max(x)}')
for k in range(K):
    print('Route', k+1,':', end=' ')
    print(*y[k], sep=' -> ', end=' | ')
    print(f'cost = {x[k]}')
