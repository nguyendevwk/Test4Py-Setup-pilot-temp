import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_updates_state():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=3, b=1, a=2, a_step=0.5)

    init_shape = woa.get_solutions().shape
    init_a = woa._a
    init_best_len = len(woa._best_solutions)

    woa.optimize()

    assert woa.get_solutions().shape == init_shape
    assert woa._a == init_a - 0.5
    assert len(woa._best_solutions) == init_best_len + 1

    best_fitness, best_sol = woa._best_solutions[0]
    assert np.isclose(best_fitness, opt_func(best_sol[0], best_sol[1]))
