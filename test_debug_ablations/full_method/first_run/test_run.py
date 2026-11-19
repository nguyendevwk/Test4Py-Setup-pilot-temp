import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_optimize_updates_internal_state():
    # deterministic random seed for reproducibility
    np.random.seed(0)

    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    nsols = 3
    b = 1.0
    a = 2.0
    a_step = 0.5

    woa = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step)

    # initial state checks
    assert woa._a == a
    assert woa._sols.shape == (nsols, 2)
    assert len(woa._best_solutions) == 0

    # run one optimization step
    woa.optimize()

    # a should be decreased by a_step
    assert woa._a == pytest.approx(a - a_step)

    # number of solutions should remain unchanged
    assert woa._sols.shape == (nsols, 2)

    # best solutions history should have one entry
    assert len(woa._best_solutions) == 1

    # the stored best solution is a tuple (fitness, solution array)
    best_fitness, best_sol = woa._best_solutions[0]
    assert isinstance(best_fitness, (float, np.floating))
    assert isinstance(best_sol, np.ndarray)
    assert best_sol.shape == (2,)
