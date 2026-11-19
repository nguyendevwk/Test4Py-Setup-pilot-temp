import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_updates_state():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=3, b=1, a=2, a_step=0.5)

    # Capture initial state
    initial_a = woa._a
    initial_sols = woa._sols.copy()

    # Run one optimization step
    woa.optimize()

    # _sols shape unchanged and contains 3 solutions of dimension 2
    assert woa._sols.shape == (3, 2)

    # _a decreased by a_step
    assert woa._a == pytest.approx(initial_a - woa._a_step)

    # All solutions respect constraints
    for sol in woa._sols:
        for (low, high), val in zip(constraints, sol):
            assert low <= val <= high

    # _best_solutions length increased by one
    assert len(woa._best_solutions) == 1

    # The stored best solution has the minimal fitness among current solutions
    fitnesses = opt_func(woa._sols[:, 0], woa._sols[:, 1])
    best_fitness = min(fitnesses)
    stored_fitness, stored_sol = woa._best_solutions[0]
    assert stored_fitness == pytest.approx(best_fitness)
    assert np.allclose(stored_sol, woa._sols[np.argmin(fitnesses)])
