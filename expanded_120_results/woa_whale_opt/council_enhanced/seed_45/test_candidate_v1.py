import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_updates_state():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-1, 1), (-1, 1)]
    woa = WhaleOptimization(opt_func, constraints, nsols=3, b=1, a=2, a_step=0.5)
    initial_sols = woa.get_solutions().copy()
    initial_a = woa._a
    fitness = opt_func(initial_sols[:, 0], initial_sols[:, 1])
    best_idx = np.argmin(fitness)
    expected_best = (fitness[best_idx], initial_sols[best_idx])
    woa.optimize()
    assert woa.get_solutions().shape == (3, 2)
    assert woa._a == pytest.approx(initial_a - woa._a_step)
    assert len(woa._best_solutions) == 1
    assert woa._best_solutions[0][0] == expected_best[0]
    assert np.allclose(woa._best_solutions[0][1], expected_best[1])
