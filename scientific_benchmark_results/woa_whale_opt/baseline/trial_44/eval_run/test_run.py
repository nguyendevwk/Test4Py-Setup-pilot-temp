import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clamps_values():
    # Setup: constraints and dummy objective
    constraints = [(-1.0, 1.0), (0.0, 5.0)]
    opt_func = lambda x, y: x + y  # simple sum, not used here
    # Instantiate with minimal parameters
    wo = WhaleOptimization(opt_func, constraints, nsols=1, b=1.0, a=1.0, a_step=0.1)

    # Solution with values outside the bounds
    sol = np.array([-5.0, 10.0])
    constrained = wo._constrain_solution(sol)

    # Expected clamped values
    expected = [-1.0, 5.0]
    assert constrained == expected, f"Expected {expected}, got {constrained}"
    # Ensure the return type is a list
    assert isinstance(constrained, list), "Return type should be a list"
    # Verify that values within bounds remain unchanged
    sol_in_bounds = np.array([0.5, 3.0])
    assert wo._constrain_solution(sol_in_bounds) == [0.5, 3.0]
