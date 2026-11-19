import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clamps_bounds():
    # Dummy objective and constraints
    opt_func = lambda x, y: np.zeros_like(x)
    constraints = [(0.0, 1.0), (0.0, 1.0)]
    # Instantiate with minimal parameters; a_step not used here
    wo = WhaleOptimization(opt_func, constraints, nsols=2, b=1.0, a=1.0, a_step=0.1)

    # Test clamping of out-of-bounds values
    out_of_bounds = [-0.5, 1.5]
    constrained = wo._constrain_solution(out_of_bounds)
    assert constrained == [0.0, 1.0], "Values should be clamped to bounds"

    # Test that values within bounds remain unchanged
    within_bounds = [0.3, 0.7]
    unchanged = wo._constrain_solution(within_bounds)
    assert unchanged == within_bounds, "Values within bounds should not change"
