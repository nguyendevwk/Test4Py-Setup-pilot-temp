import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_state_transition():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=3, b=1, a=2, a_step=0.1)

    # Record initial state
    init_a = woa._a
    init_shape = woa._sols.shape
    init_best_len = len(woa._best_solutions)
    init_fitness = np.min(opt_func(woa._sols[:, 0], woa._sols[:, 1]))

    # Run one optimization step
    woa.optimize()

    # Verify state transitions
    assert woa._a == init_a - woa._a_step, "Parameter 'a' did not decrement correctly."
    assert woa._sols.shape == init_shape, "Solution shape changed unexpectedly."
    assert len(woa._best_solutions) == init_best_len + 1, "Best solutions history not updated."

    # Verify new best fitness is not worse than previous best
    new_fitness = np.min(opt_func(woa._sols[:, 0], woa._sols[:, 1]))
    assert new_fitness <= init_fitness, "New best fitness is worse than previous best."

    # Verify that the stored best solution matches the computed best
    stored_fitness, stored_solution = woa._best_solutions[-1]
    assert np.isclose(stored_fitness, new_fitness), "Stored best fitness does not match computed best."
    assert np.allclose(stored_solution, woa._sols[np.argmin(opt_func(woa._sols[:, 0], woa._sols[:, 1]))]), \
        "Stored best solution does not match the best solution in current population."
