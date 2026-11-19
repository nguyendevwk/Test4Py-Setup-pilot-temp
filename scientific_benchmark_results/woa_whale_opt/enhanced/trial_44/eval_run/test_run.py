import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_optimize_decreases_a_and_preserves_best_solution():
    np.random.seed(0)  # deterministic randomness
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    nsols = 3
    b, a, a_step = 1.0, 2.0, 0.5

    woa = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step)
    original_sols = woa._sols.copy()

    # Determine best solution before optimization
    fitness = opt_func(original_sols[:, 0], original_sols[:, 1])
    best_idx = np.argmin(fitness)
    best_sol = original_sols[best_idx]

    initial_a = woa._a
    woa.optimize()

    # a should be reduced by a_step
    assert woa._a == pytest.approx(initial_a - a_step)

    # number of solutions and dimensionality unchanged
    assert woa._sols.shape == (nsols, 2)

    # first solution in new generation is the previous best solution
    assert np.allclose(woa._sols[0], best_sol)
