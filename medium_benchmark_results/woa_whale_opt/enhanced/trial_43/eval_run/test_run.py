import pytest
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clipping():
    # Setup a simple optimizer with known constraints
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-1, 1), (0, 2)]
    woa = WhaleOptimization(opt_func, constraints, nsols=3, b=1, a=2, a_step=0.1)

    # Test values outside the bounds are clipped to the nearest bound
    out_of_bounds = [-2, 3]
    constrained = woa._constrain_solution(out_of_bounds)
    assert constrained == [-1, 2], f"Expected [-1, 2], got {constrained}"

    # Test values within the bounds remain unchanged
    in_bounds = [0.5, 1.5]
    unchanged = woa._constrain_solution(in_bounds)
    assert unchanged == in_bounds, f"Expected {in_bounds}, got {unchanged}"
