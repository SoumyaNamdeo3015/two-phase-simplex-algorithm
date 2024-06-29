# Two-Phase Simplex Algorithm

## About the Algorithm
The simplex algorithm is a popular method for solving linear programming problems. It is used to find the optimal value of an objective function given a set of linear inequalities or equations as constraints.

For more detailed information, refer to the [Simplex algorithm](https://en.wikipedia.org/wiki/Simplex_algorithm) on Wikipedia.

## Input File (input.txt)
The input file `input.txt` should be formatted as follows:

1. The first two lines indicate the type of linear programming problem:
   - `max` for maximization problems
   - `min` for minimization problems
2. The matrix \( A \) representing the coefficients of the constraints.
3. The matrix \( b \) representing the right-hand side values of the constraints.
4. The constraint types, which can be one of `>=`, `<=`, or `=`.
5. The matrix \( c \) representing the cost vector.


## Main Python Script (main.py)
The main Python script `main.py` should contain a single function named `simplex_algo`. This function reads the input from `input.txt` and solves the linear programming problem using the two-phase simplex algorithm.

### Function: `simplex_algo`
The `simplex_algo` function returns a dictionary with the following keys and values:

- **`initial_tableau`**: Stores the initial tableau.
- **`final_tableau`**: Stores the final tableau.
- **`solution_status`**: Stores the status of the solution (`'unbounded'`, `'optimal'`, or `'infeasible'`).
- **`optimal_solution`**: Stores the optimal solution vector as a Python list.
- **`optimal_value`**: Stores the cost at the optimal solution vector.

### Example of the `simplex_algo` Function
```python
def simplex_algo():
    # Read the input file and implement the two-phase simplex algorithm here
    # This is a placeholder for the actual implementation

    # Example return value
    return {
        'initial_tableau': initial_tableau,
        'final_tableau': final_tableau,
        'solution_status': solution_status,
        'optimal_solution': optimal_solution,
        'optimal_value': optimal_value
    }

