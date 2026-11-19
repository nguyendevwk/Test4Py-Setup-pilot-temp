import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_updates_and_constraints():
    # deterministic random seed
    np.random.seed(0)

    # simple objective: sum of squares (minimization)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(0.0, 1.0), (0.0, 1.0)]
    nsols = 5
    b, a, a_step = 1.0, 2.0, 0.5

    optimizer = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step, maximize=False)

    # Capture initial state
    initial_sols = optimizer.get_solutions().copy()
    len_before = len(optimizer._best_solutions)

    # Get best solution before optimization
    best_sol = optimizer._rank_solutions()[0]

    # Run one optimization step
    optimizer.optimize()

    # After optimization, number of solutions should remain unchanged
    assert optimizer.get_solutions().shape == initial_sols.shape

    # Parameter 'a' should have decreased by a_step
    assert optimizer._a == a - a_step

    # The first solution in the new generation should be the previous best solution
    assert np.allclose(optimizer.get_solutions()[0], best_sol)

    # Best solutions history should have grown by one entry
    assert len(optimizer._best_solutions) == len_before + 1
    # The first entry in history should still be the previous best solution
    assert np.allclose(optimizer._best_solutions[0], best_sol)

    # All solutions must respect the constraints
    lower_bounds = np.array([c[0] for c in constraints])
    upper_bounds = np.array([c[1] for c in constraints])
    assert np.all(optimizer.get_solutions() >= lower_bounds)
    assert np.all(optimizer.get_solutions() <= upper_bounds)
