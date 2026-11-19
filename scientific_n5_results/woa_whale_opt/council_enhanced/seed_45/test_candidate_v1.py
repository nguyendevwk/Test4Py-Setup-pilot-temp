import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_state():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=5, b=1, a=2, a_step=0.1)

    initial_a = woa._a
    initial_sols = woa._sols.copy()

    woa.optimize()

    # a decreases by a_step
    assert woa._a == pytest.approx(initial_a - woa._a_step)

    # best_solutions length increases by 1
    assert len(woa._best_solutions) == 1

    # shape of solutions remains unchanged
    assert woa._sols.shape == initial_sols.shape

    # all solutions respect constraints
    for sol in woa._sols:
        for (low, high), val in zip(constraints, sol):
            assert low <= val <= high

    # best solution fitness is minimal among current generation
    fitness = opt_func(woa._sols[:, 0], woa._sols[:, 1])
    best_fitness, best_sol = woa._best_solutions[0]
    assert best_fitness == pytest.approx(fitness.min())
    # best solution equals the one with minimal fitness
    assert np.allclose(best_sol, woa._sols[fitness.argmin()])
