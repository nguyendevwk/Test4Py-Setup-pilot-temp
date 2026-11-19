import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_optimize_includes_best_and_updates_a():
    np.random.seed(0)
    # simple objective: minimize sum of squares
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-1, 1), (-1, 1)]
    nsols = 3
    b = 1.0
    a = 1.0
    a_step = 0.1

    wo = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step, maximize=False)

    # Capture initial state
    initial_sols = wo.get_solutions().copy()
    initial_a = wo._a
    # Compute best solution before optimization
    fitness = opt_func(initial_sols[:, 0], initial_sols[:, 1])
    best_index = np.argmin(fitness)
    best_before = initial_sols[best_index]

    # Run one optimization step
    wo.optimize()

    # After optimization, a should have decreased by a_step
    assert wo._a == pytest.approx(initial_a - a_step)

    # The first solution in the new population should be the previous best
    new_sols = wo.get_solutions()
    assert new_sols.shape == (nsols, 2)
    assert np.allclose(new_sols[0], best_before)

    # The best solutions history should have grown by one entry
    assert len(wo._best_solutions) == 1
    # The stored best should match the best before (since we only ran one generation)
    assert np.allclose(wo._best_solutions[0][1], best_before)
