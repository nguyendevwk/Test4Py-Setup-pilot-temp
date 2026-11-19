import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_updates_state_and_constraints():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=3, b=1, a=2, a_step=0.5)

    initial_a = woa._a
    initial_sols = woa.get_solutions().copy()

    woa.optimize()

    # a decreased by a_step
    assert woa._a == pytest.approx(initial_a - 0.5)

    # shape of solutions unchanged
    assert woa.get_solutions().shape == initial_sols.shape

    # all solutions respect constraints
    for sol in woa.get_solutions():
        assert -5 <= sol[0] <= 5
        assert -5 <= sol[1] <= 5

    # best solutions history updated
    assert len(woa._best_solutions) == 1
    best_fitness, best_sol = woa._best_solutions[0]
    assert -5 <= best_sol[0] <= 5
    assert -5 <= best_sol[1] <= 5
