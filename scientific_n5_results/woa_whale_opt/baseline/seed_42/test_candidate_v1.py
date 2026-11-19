import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_optimize_includes_best_solution_and_updates_a_and_constraints():
    np.random.seed(0)
    opt_func = lambda x, y: x + y
    constraints = [[0, 1], [0, 1]]
    nsols = 5
    a = 1.0
    a_step = 0.2
    b = 1.0
    whale = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step, maximize=False)

    sols = whale.get_solutions()
    fitness = opt_func(sols[:, 0], sols[:, 1])
    best_idx = np.argmin(fitness)
    best_sol_before = sols[best_idx]
    a_before = whale._a

    whale.optimize()

    # First solution should be the previous best
    assert np.allclose(whale.get_solutions()[0], best_sol_before)
    # a should decrease by a_step
    assert whale._a == a_before - a_step
    # All solutions must respect constraints
    for dim, (low, high) in enumerate(constraints):
        assert np.all(whale.get_solutions()[:, dim] >= low)
        assert np.all(whale.get_solutions()[:, dim] <= high)
