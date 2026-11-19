import pytest
import numpy as np
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_basic_behavior():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=3, b=1, a=2, a_step=0.1)
    initial_a = woa._a
    initial_sols = woa.get_solutions().copy()
    woa.optimize()
    # a should decrease by a_step
    assert woa._a == pytest.approx(initial_a - woa._a_step)
    # number of solutions unchanged
    assert woa.get_solutions().shape == initial_sols.shape
    # all solutions within constraints
    for sol in woa.get_solutions():
        assert constraints[0][0] <= sol[0] <= constraints[0][1]
        assert constraints[1][0] <= sol[1] <= constraints[1][1]
    # best_solutions list updated
    assert len(woa._best_solutions) == 1
    best_fitness, best_sol = woa._best_solutions[0]
    # best fitness should equal the minimum of current fitnesses
    current_fitness = opt_func(woa.get_solutions()[:, 0], woa.get_solutions()[:, 1])
    assert best_fitness == pytest.approx(np.min(current_fitness))
