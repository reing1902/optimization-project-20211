import numpy as np

def heuristic_greedy(data):
    '''
    Solve the problem using a greedy heuristic.
    Heuristic: Assign the job with the smallest travel time + fix time 
    to the technician with the smallest number of jobs.

    Parameters
    ----------
    data : Data
        The data to be used in the problem.
    '''
    # Initialize the solution
    x = np.array([0 for k in range(data.K)]) # working time of staff k
    y = {k:[0] for k in range(data.K)} # customers that staff k serves

    customers = [n for n in range(1, data.N+1)]
    while len(customers) != 0:
        # Find the technician with the smallest number of jobs
        staff = np.argmin(x)

        # Find the last customer that the technician served
        i = y[staff][-1]

        # Find the next customer with the smallest travel time + fix time
        knowledge = []
        for l in customers:
            knowledge.append((l, data.t[i][l] + data.d[l-1]))
        knowledge.sort(key = lambda item: item[1])

        # Assign that customer to the technician and update the solution
        j = knowledge[0][0]
        y[staff].append(j)
        x[staff] += knowledge[0][1]

        # Remove the customer from the list of customers
        customers.remove(j)

    for k in range(data.K):
        x[k] += data.t[y[k][-1]][0]
        y[k].append(0)

    print(f'Optimal cost: {np.max(x)}')
    for k in range(data.K):
        print('Route', k+1,':', end=' ')
        print(*y[k], sep=' -> ', end=' | ')
        print(f'cost = {x[k]}')
