import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_optimize_includes_best_and_updates_state():
    # deterministic random seed
    np.random.seed(42)

    # simple objective: sum of coordinates (minimization)
    opt_func = lambda x, y: x + y
    constraints = [(0.0, 1.0), (0.0, 1.0)]
    nsols = 3
    b = 1.0
    a = 1.0
    a_step = 0.1

    wo = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step, maximize=False)

    # capture initial state
    initial_sols = wo.get_solutions().copy()
    initial_a = wo._a
    # rank solutions to find current best
    ranked = wo._rank_solutions()
    best_before = ranked[0]

    # run one optimization step
    wo.optimize()

    # after optimization, shape should remain unchanged
    assert wo.get_solutions().shape == initial_sols.shape

    # a should be decreased by a_step
    assert wo._a == pytest.approx(initial_a - a_step)

    # best solution should be first element in new population
    new_sols = wo.get_solutions()
    assert np.allclose(new_sols[0], best_before)

    # history of best solutions should have grown by one
    assert len(wo._best_solutions) == 1
