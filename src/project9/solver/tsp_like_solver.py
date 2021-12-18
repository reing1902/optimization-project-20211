from ortools.linear_solver import pywraplp

def tsp_like_solver(data):
    '''
    Solve the scheduling problem using the IP solver.

    Parameters
    ----------
    data : Data
        The data to be used in the problem.
    '''

    # Duplicate the source node K times
    d = data.d + [0] * data.K
    t = [data.t[i] + [data.t[i][0]] * data.K for i in range(data.N+1)]
    [t.append(t[0]) for _ in range(data.K)]
    N = data.N + data.K + 1
    K = data.K 

    def create_solver_variables():
        '''
        Create the IP solver and variables
        
        Returns
        -------
        solver : Solver
            The solver to be used.
        x : list of list of list of IntVar
            The variables for the scheduling problem.
        '''
        solver = pywraplp.Solver.CreateSolver('CBC')
        
        # Create the variables
        x = [[solver.IntVar(0, 1, f'x[{i}][{j}]') for j in range(N)] for i in range(N)]

        total_fix_time = sum(data.d)
        total_travel_time = sum(sum(i) for i in data.t)
        # Working time = Fix time + Travel time at each node
        z = [solver.IntVar(0, total_fix_time + total_travel_time, f'z({u})') for u in range(N)]
        # The maximum working time of a technician
        w = solver.IntVar(0, total_fix_time + total_travel_time, 'w')

        return solver, x, z, w

    def add_balance_flow_constraints(solver, x):
        '''
        Add the balance flow constraints to the solver.

        Parameters
        ----------
        solver : Solver
            The solver to be used.
        x : list of list of list of IntVar
            The variables for the scheduling problem.
        '''
        for k in range(N):
            c1 = solver.Constraint(1, 1)
            [c1.SetCoefficient(x[i][k], 1) for i in range(N) if i != k]

            c2 = solver.Constraint(1, 1)
            [c2.SetCoefficient(x[k][i], 1) for i in range(N) if i != k]

    def solve_with_given_SEC(SECs):
        '''
        Solve the scheduling problem (TSP-like) using the given SEC.

        Parameters
        ----------
        SECs : list of list of int
            The SECs to be used.

        Returns
        -------
        solution: list of lists of int
            The value of binary variables
        objective_value: int
            The objective value of the solution
        '''
        solver, x, z, w = create_solver_variables()
        add_balance_flow_constraints(solver, x)

        # Source nodes constraints
        for i in range(N-K, N-1):
            c9 = solver.Constraint(0, 0)
            c9.SetCoefficient(x[0][i], 1)
            c10 = solver.Constraint(0, 0)
            c10.SetCoefficient(x[i][0], 1)
            c11 = solver.Constraint(0, 0)
            c11.SetCoefficient(x[i][N-1], 1)
            c12 = solver.Constraint(0, 0)
            c12.SetCoefficient(x[N-1][i], 1)
        
        c4 = solver.Constraint(1, 1)
        c4.SetCoefficient(x[N-1][0], 1)

        # Add the SEC constraints
        for C in SECs:
            c5 = solver.Constraint(0, len(C)-1)
            [c5.SetCoefficient(x[i][j], 1) for i in C for j in C if j != i]

        # Add constraints on z and w
        c = solver.Constraint(0, 0)
        c.SetCoefficient(z[0], 1)

        INF = solver.infinity()
        M = sum(sum(i) for i in data.t) + sum(data.d)

        for i in range(N):
            for j in range(1, N):
                if i != j:
                    # M(1 - x[i][j]) + z[j] >= z[i] + d[j] + t[i][j]
                    c6 = solver.Constraint(-M + d[j] + t[i][j], INF)
                    c6.SetCoefficient(x[i][j], -M)
                    c6.SetCoefficient(z[j], 1)
                    c6.SetCoefficient(z[i], -1)

                    # M(x[i][j] - 1) + z[j] <= z[i] + d[j] + t[i][j]
                    c7 = solver.Constraint(-M - d[j] - t[i][j], INF)
                    c7.SetCoefficient(x[i][j], -M)
                    c7.SetCoefficient(z[i], 1)
                    c7.SetCoefficient(z[j], -1)

        for i in range(N-K+1, N):
            c8 = solver.Constraint(0, INF)
            c8.SetCoefficient(z[i], -1)
            c8.SetCoefficient(z[i-1], 1)
            c8.SetCoefficient(w, 1)

        c8 = solver.Constraint(0, INF)
        c8.SetCoefficient(z[N-K], -1)
        c8.SetCoefficient(w, 1)

        print(f'Solving with SECs: {SECs}')
        # Create the objective function
        obj = solver.Objective()
        obj.SetCoefficient(w, 1)
        obj.SetMinimization()

        # Solve the problem
        solver.Solve()
        solution = [[x[i][j].solution_value() for j in range(N)] for i in range(N)]
        objective_value = obj.Value()

        return solution, objective_value

    def findNext(s, x):
        for i in range(N):
            if i != s and x[s][i] == 1:
                return i
        return -1

    def extract_subtour(s, x):
        C = []
        C.append(s)
        while True:
            i = findNext(s, x)
            if i == -1:
                return None
            if i in C:
                return C
            C.append(i)
            s = i

    def solve_TSP():
        SECs = []
        while True:
            solution, objective_value = solve_with_given_SEC(SECs)
            print(f'Found solution with objective value {objective_value}')

            # Discover sub-tours of the solution
            visited = [False] * N
            for i in range(N):
                if visited[i]:
                    continue
                C = extract_subtour(i, solution)
                print(f'Found subtour {C}')
                if len(C) == N:
                    print('Found the optimal solution')
                    print(*C, sep=' -> ', end=f' -> {C[0]}, ')
                    return C
                
                SECs.append(C)
                for j in C:
                    visited[j] = True

    return solve_TSP()