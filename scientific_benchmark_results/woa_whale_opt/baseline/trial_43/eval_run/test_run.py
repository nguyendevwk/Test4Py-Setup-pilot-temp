import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_updates_state():
    # simple fitness: sum of coordinates
    opt_func = lambda x, y: x + y
    constraints = [(-10, 10), (-10, 10)]
    nsols = 3
    b = 1.0
    a = 2.0
    a_step = 0.5

    wo = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step, maximize=False)

    # initial state
    assert wo._a == a
    assert wo._best_solutions == []

    # run one optimization step
    wo.optimize()

    # a should have decreased by a_step
    assert wo._a == pytest.approx(a - a_step)

    # solutions shape unchanged
    assert wo._sols.shape == (nsols, 2)

    # best solutions list should have one entry
    assert len(wo._best_solutions) == 1

    # best solution stored correctly
    best_fitness, best_sol = wo._best_solutions[0]
    expected_fitness = opt_func(best_sol[0], best_sol[1])
    assert best_fitness == pytest.approx(expected_fitness)
