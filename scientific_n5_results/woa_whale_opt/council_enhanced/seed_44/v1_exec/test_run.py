import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_updates_state():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=5, b=1, a=2, a_step=0.1)

    # initial state
    init_sols = woa.get_solutions()
    assert init_sols.shape == (5, 2)
    assert np.all((init_sols >= -5) & (init_sols <= 5))
    assert woa._a == 2
    assert len(woa._best_solutions) == 0

    woa.optimize()

    # after one optimization step
    new_sols = woa.get_solutions()
    assert new_sols.shape == (5, 2)
    assert np.all((new_sols >= -5) & (new_sols <= 5))
    assert woa._a == 1.9  # decreased by a_step
    assert len(woa._best_solutions) == 1

    # best solution should be the one with minimal fitness
    best_fitness, best_sol = woa._best_solutions[0]
    computed_fitness = opt_func(best_sol[0], best_sol[1])
    assert pytest.approx(best_fitness) == computed_fitness
