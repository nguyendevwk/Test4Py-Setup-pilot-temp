import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_optimize_includes_best_and_updates_state():
    # deterministic random seed
    np.random.seed(42)

    # simple objective: sum of coordinates (minimization)
    opt_func = lambda x, y: x + y
    constraints = [(-1.0, 1.0), (-1.0, 1.0)]
    nsols = 3
    b, a, a_step = 1.0, 2.0, 0.5

    whale = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step, maximize=False)

    # capture initial state
    initial_sols = whale.get_solutions().copy()
    initial_a = whale._a

    # compute best solution before optimization
    fitness = opt_func(initial_sols[:, 0], initial_sols[:, 1])
    best_idx = np.argmin(fitness)  # minimize
    best_sol = initial_sols[best_idx]

    # run one optimization step
    whale.optimize()

    # after optimization, number of solutions should remain unchanged
    assert whale.get_solutions().shape == (nsols, 2)

    # the first solution should be the previous best solution
    np.testing.assert_array_almost_equal(whale.get_solutions()[0], best_sol, decimal=6)

    # the internal a parameter should have decreased by a_step
    assert pytest.approx(whale._a, rel=1e-6) == initial_a - a_step

    # best_solutions history should have one entry
    assert len(whale._best_solutions) == 1
    # the stored best solution should match the best before optimization
    stored_best = whale._best_solutions[0]
    np.testing.assert_array_almost_equal(stored_best[1], best_sol, decimal=6)
