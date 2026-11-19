import pytest
import numpy as np
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clamps_values():
    # Dummy objective function and constraints
    opt_func = lambda x, y: x + y
    constraints = [(0.0, 1.0), (-2.0, 2.0)]
    # Instantiate WhaleOptimization (parameters other than constraints are irrelevant for this test)
    wo = WhaleOptimization(opt_func, constraints, nsols=1, b=1.0, a=1.0, a_step=0.1)

    # Test values below lower bounds
    sol_low = [-0.5, -3.0]
    constrained_low = wo._constrain_solution(sol_low)
    assert constrained_low == [0.0, -2.0], "Values below lower bounds should be clamped to lower limits"

    # Test values above upper bounds
    sol_high = [1.5, 3.0]
    constrained_high = wo._constrain_solution(sol_high)
    assert constrained_high == [1.0, 2.0], "Values above upper bounds should be clamped to upper limits"

    # Test values within bounds remain unchanged
    sol_mid = [0.5, 0.0]
    constrained_mid = wo._constrain_solution(sol_mid)
    assert constrained_mid == [0.5, 0.0], "Values within bounds should remain unchanged"

    # Ensure the returned object is a list, not a numpy array
    assert isinstance(constrained_mid, list), "Constrained solution should be returned as a list"

    # Original input should not be modified
    assert sol_mid == [0.5, 0.0], "Input list should remain unchanged after constraining"
