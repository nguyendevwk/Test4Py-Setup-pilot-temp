import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_optimize_updates_solutions_and_a_and_best_history():
    # deterministic randomness
    np.random.seed(42)

    # simple objective: sum of squares
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    nsols = 3
    b = 1.0
    a = 2.0
    a_step = 0.5

    wo = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step, maximize=False)

    # initial state
    initial_a = wo._a
    initial_sols_shape = wo._sols.shape
    assert wo._best_solutions == []

    # run one optimization step
    wo.optimize()

    # a should have decreased by a_step
    assert wo._a == pytest.approx(initial_a - a_step)

    # number of solutions unchanged
    assert wo._sols.shape == initial_sols_shape

    # all solutions respect constraints
    for sol in wo._sols:
        for (low, high), val in zip(constraints, sol):
            assert low <= val <= high

    # best_solutions history updated
    assert len(wo._best_solutions) == 1
    best_fitness, best_sol = wo._best_solutions[0]
    # fitness should match evaluation of best solution
    expected_fitness = opt_func(best_sol[0], best_sol[1])
    assert best_fitness == pytest.approx(expected_fitness)
    # solution shape should be 2
    assert best_sol.shape == (2,)
