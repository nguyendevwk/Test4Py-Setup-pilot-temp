import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_state_transition():
    # deterministic random numbers
    np.random.seed(0)

    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    nsols = 4
    b, a, a_step = 1.0, 2.0, 0.1

    woa = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step, maximize=False)

    init_a = woa._a
    init_shape = woa._sols.shape
    init_best_len = len(woa._best_solutions)

    woa.optimize()

    # a should decrease by a_step
    assert woa._a == pytest.approx(init_a - a_step)

    # shape of solutions remains unchanged
    assert woa._sols.shape == init_shape

    # best_solutions list should have grown by one
    assert len(woa._best_solutions) == init_best_len + 1

    # the appended best solution is a tuple (fitness, solution array)
    best_fitness, best_sol = woa._best_solutions[-1]
    assert isinstance(best_fitness, float)
    assert isinstance(best_sol, np.ndarray)
    assert best_sol.shape == (2,)
