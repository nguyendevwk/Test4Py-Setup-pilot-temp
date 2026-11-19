import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_state_transition():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-1, 1), (-1, 1)]
    woa = WhaleOptimization(opt_func, constraints, nsols=3, b=1, a=2, a_step=0.5)
    old_a = woa._a
    woa.optimize()
    # a should decrease by a_step
    assert woa._a == pytest.approx(old_a - 0.5)
    # best solution history should have one entry
    assert len(woa._best_solutions) == 1
    # first solution in new population should be the best solution
    best_sol = woa._best_solutions[0]
    assert woa._sols.shape == (3, 2)
    np.testing.assert_allclose(woa._sols[0], best_sol, atol=1e-8)
