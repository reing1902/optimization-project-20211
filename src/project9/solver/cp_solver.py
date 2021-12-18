from ortools.sat.python import cp_model

def cp_solver(data):
    '''
    Solve the scheduling problem using the CP solver.

    Parameters
    ----------
    data : Data
        The data to be used in the problem.
    '''
    class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
        #print intermediate solution
        def __init__(self, variables):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self.__variables = variables
            self.__solution_count = 0

        def on_solution_callback(self):
            self.__solution_count += 1
            for v in self.__variables:
                print('%s = %i'% (v, self.Value(v)), end = ' ')
            print()

        def solution_count(self):
            return self.__solution_count

    model = cp_model.CpModel()

    total_fix_time = sum(data.d)
    total_travel_time = sum(sum(i) for i in data.t)

    x = [[[model.NewIntVar(0, 1, f'x({u}, {i}, {j})') for j in range(data.N+1)] for i in range(data.N+1)] for u in range(data.K)]
    y = [model.NewIntVar(0, total_fix_time, f'y({u})') for u in range(data.K)]
    z = [model.NewIntVar(0, total_fix_time + total_travel_time, f'z({u})') for u in range(data.K)]
    w = model.NewIntVar(0, total_fix_time + total_travel_time, 'w')

    for i in range(1, data.N+1):
        model.Add(sum(x[k][i][j] for k in range(data.K) for j in range(data.N+1) if j != i) == 1)

    for j in range(1, data.N+1):
        model.Add(sum(x[k][i][j] for k in range(data.K) for i in range(data.N+1) if j != i) == 1)

    for l in range(data.N+1):
        for k in range(data.K):
            to_l = (x[k][i][l] for i in range(data.N+1) if i != l)
            out_l = (x[k][l][j] for j in range(data.N+1) if j != l)
            model.Add(sum(to_l) == sum(out_l))

    for k in range(data.K):
        model.Add(sum(x[k][0][j] for j in range(1, data.N+1)) == 1)

    for k in range(data.K):
        model.Add(sum(x[k][i][0] for i in range(1, data.N+1)) == 1)

    for k in range(data.K):
        model.Add(sum(x[k][i][j]*data.d[j] for i in range(data.N+1) for j in range(1, data.N+1) if i != j) == y[k])

    for k in range(data.K):
        model.Add(sum(x[k][i][j]*data.t[i][j] for i in range(data.N+1) for j in range(1, data.N+1) if i != j) + y[k] == z[k])

    for k in range(data.K):
        model.Add(w >= z[k])

    model.Minimize(w)

    solver = cp_model.CpSolver()

    solution_printer = VarArraySolutionPrinter([w])

    solver.parameters.enumerate_all_solutions = True

    status = solver.Solve(model, solution_printer)

    print('Status = %s' % solver.StatusName(status))
    print('Number of solutions found: %i' % solution_printer.solution_count())