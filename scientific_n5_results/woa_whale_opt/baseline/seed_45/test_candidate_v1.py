import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_updates_solutions_and_a():
    # deterministic random seed
    np.random.seed(0)

    # simple objective: sum of coordinates (minimization)
    def opt_func(x, y):
        return x + y

    constraints = [(-1.0, 1.0), (-1.0, 1.0)]
    nsols = 3
    b = 1.0
    a = 2.0
    a_step = 0.5

    wo = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step, maximize=False)

    # capture initial state
    initial_a = wo._a
    initial_sols = wo.get_solutions().copy()

    # run one optimization step
    wo.optimize()

    # after optimization, number of solutions unchanged
    assert wo.get_solutions().shape == (nsols, 2)

    # a decreased by a_step
    assert wo._a == pytest.approx(initial_a - a_step)

    # best solution from previous generation is included in new generation
    best_fitness, best_sol = wo._best_solutions[-1]
    # best_sol is a 1D array of length 2
    assert any(np.allclose(wo.get_solutions()[i], best_sol) for i in range(nsols))

    # all solutions respect constraints
    for sol in wo.get_solutions():
        for val, (low, high) in zip(sol, constraints):
            assert low <= val <= high
