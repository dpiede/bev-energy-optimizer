"""Sanity check that CVXPY and its solvers are installed and working.

Run with: uv run python -m bev.solver_check
"""

import cvxpy as cp


def solve_toy_lp() -> float:
    """Minimise x + y subject to x >= 1, y >= 2. Optimum is 3."""
    x = cp.Variable()
    y = cp.Variable()
    problem = cp.Problem(cp.Minimize(x + y), [x >= 1, y >= 2])
    problem.solve()
    assert problem.status == cp.OPTIMAL, problem.status
    return float(problem.value)


def main() -> None:
    print(f"CVXPY {cp.__version__}")
    print(f"Installed solvers: {cp.installed_solvers()}")
    print(f"Toy LP optimum: {solve_toy_lp():.4f} (expected 3.0)")


if __name__ == "__main__":
    main()
