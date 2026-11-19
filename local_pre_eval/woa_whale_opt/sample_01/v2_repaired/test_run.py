import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_rank_and_constrain_behavior():
    # Define a simple objective: sum of squares
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-10, 10), (-10, 10)]
    woa = WhaleOptimization(opt_func, constraints, nsols=3, b=1, a=2, a_step=0.1)

    # Manually set solutions to known values
    woa._sols = np.array([[3, 4], [1, 1], [5, 5]])  # shape (3,2)

    # Rank solutions and capture best
    ranked = woa._rank_solutions()
    # Expected order: [1,1] (fitness 2), [3,4] (25), [5,5] (50)
    assert ranked[0].tolist() == [1, 1]
    assert ranked[1].tolist() == [3, 4]
    assert ranked[2].tolist() == [5, 5]

    # Best solution stored in history
    assert len(woa._best_solutions) == 1
    best_fitness, best_sol = woa._best_solutions[0]
    assert best_fitness == 2
    assert best_sol.tolist() == [1, 1]

    # Test constraint enforcement: clamp values outside bounds
    out_of_bounds = np.array([12, -12])
    constrained = woa._constrain_solution(out_of_bounds)
    assert constrained == [-10, 10]
