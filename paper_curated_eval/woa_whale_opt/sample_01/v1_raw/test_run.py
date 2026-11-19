import numpy as np
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_updates_state_and_best_solution():
    np.random.seed(0)
    constraints = [(-5, 5), (-5, 5)]
    opt_func = lambda x, y: np.sum(x**2) + np.sum(y**2)
    wo = WhaleOptimization(opt_func, constraints, nsols=5, b=1, a=2, a_step=0.1)

    # Determine best solution from initial population
    init_sols = wo._sols
    fitness = opt_func(init_sols[:, 0], init_sols[:, 1])
    best_idx = np.argmin(fitness)
    best_sol = init_sols[best_idx]
    best_fitness = fitness[best_idx]

    # Run one optimization step
    wo.optimize()

    # Check that a decreased
    assert wo._a == 2 - 0.1

    # Check that number of solutions unchanged
    assert wo._sols.shape == (5, 2)

    # Check that best solution is first in new population
    assert np.allclose(wo._sols[0], best_sol)

    # Check that best solution history recorded correctly
    recorded_fitness, recorded_sol = wo._best_solutions[0]
    assert recorded_fitness == best_fitness
    assert np.allclose(recorded_sol, best_sol)
