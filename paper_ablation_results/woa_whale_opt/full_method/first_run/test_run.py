import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clipping():
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=1, b=1, a=2, a_step=0.1)

    # Solution exceeding upper and lower bounds
    sol = np.array([10.0, -10.0])
    constrained = woa._constrain_solution(sol)
    assert constrained == [5.0, -5.0], "Values should be clipped to bounds"

    # Solution within bounds should remain unchanged
    sol2 = np.array([3.0, -4.0])
    constrained2 = woa._constrain_solution(sol2)
    assert constrained2 == [3.0, -4.0], "Values within bounds should not change"
