import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_rank_solutions_appends_best_and_returns_sorted():
    np.random.seed(42)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=5, b=1, a=2, a_step=0.1)

    # Capture current solutions and compute expected best solution
    sols = woa.get_solutions()
    fitness = opt_func(sols[:, 0], sols[:, 1])
    best_idx = np.argmin(fitness)  # minimize fitness
    expected_best = sols[best_idx]

    # Call _rank_solutions and inspect results
    ranked = woa._rank_solutions()

    # Check that returned list contains all solutions sorted by fitness
    sorted_fitness = np.sort(fitness)
    returned_fitness = opt_func(np.array(ranked)[:, 0], np.array(ranked)[:, 1])
    np.testing.assert_allclose(returned_fitness, sorted_fitness, atol=1e-12)

    # Check that best solution was appended to _best_solutions
    assert len(woa._best_solutions) == 1
    np.testing.assert_allclose(woa._best_solutions[0][1], expected_best, atol=1e-12)
