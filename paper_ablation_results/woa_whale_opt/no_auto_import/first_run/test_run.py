import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clips_out_of_bounds():
    # Setup: constraints that force clipping
    constraints = [(-1.0, 1.0), (2.0, 4.0)]
    # Dummy objective function (unused in this test)
    opt_func = lambda x, y: x**2 + y**2
    # Instantiate with minimal parameters
    woa = WhaleOptimization(opt_func, constraints, nsols=1, b=1.0, a=2.0, a_step=0.1)

    # Solution with values outside the specified bounds
    out_of_bounds = np.array([-2.0, 5.0])
    constrained = woa._constrain_solution(out_of_bounds)

    # Expected clipped values
    expected = [-1.0, 4.0]
    assert constrained == expected, f"Expected {expected}, got {constrained}"
    # Ensure the result is a list of floats
    assert isinstance(constrained, list)
    assert all(isinstance(v, float) for v in constrained)
