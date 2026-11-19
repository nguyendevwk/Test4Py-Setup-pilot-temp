import pytest
import numpy as np
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clamps_bounds():
    # Setup: simple quadratic objective, two constraints
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-10, 10)]
    woa = WhaleOptimization(opt_func, constraints, nsols=3, b=1, a=2, a_step=0.1)

    # Case 1: values outside bounds
    out_of_bounds = [6.0, -15.0]  # first >5, second < -10
    constrained = woa._constrain_solution(out_of_bounds)
    assert constrained == [5.0, -10.0], "Values should be clamped to bounds"

    # Case 2: values inside bounds remain unchanged
    inside = [0.0, 0.0]
    constrained_inside = woa._constrain_solution(inside)
    assert constrained_inside == [0.0, 0.0], "Values inside bounds should stay the same"

    # Ensure original list is not modified
    assert out_of_bounds == [6.0, -15.0], "Original list should remain unchanged"
