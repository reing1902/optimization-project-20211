# Project 9 for the course IT3052E - Fundamentals of optimization

## Installation
Download the package or clone the repository, and then install with:

```bash
pip install -e <path-to-the-clone-repo>
```

## Import / Generate data

```
from project9.data import Data

# Import data from file
imported_data = Data.from_file('N6-K2.txt')

# Generate data object using the given parameters
generated_data = Data.generated_with(N=6, K=2, seed=42)
```

## Solvers
```
from project9.solver import ip_solver, cp_solver

# Solve the problem using the CP solver
cp_solver(imported_data)

# Solve the problem using the IP solver
ip_solver(generated_data)
```