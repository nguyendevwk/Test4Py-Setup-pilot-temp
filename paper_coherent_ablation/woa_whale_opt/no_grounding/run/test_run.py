import pytest
import numpy as np
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clipping():
    # Dummy objective function
    opt_func = lambda x, y: x + y
    constraints = [(0, 1), (0, 1)]
    whale = WhaleOptimization(opt_func, constraints, nsols=1, b=1.0, a=1.0, a_step=0.1)

    # Out‑of‑bounds solution should be clipped to the bounds
    out_of_bounds = [-0.5, 1.5]
    clipped = whale._constrain_solution(out_of_bounds)
    assert clipped == [0, 1], "Values should be clipped to the bounds"

    # In‑bounds solution should remain unchanged
    in_bounds = [0.3, 0.7]
    unchanged = whale._constrain_solution(in_bounds)
    assert unchanged == in_bounds, "In‑bounds values should not be altered"

    # Ensure the original list is not modified
    original = [0.3, 0.7]
    _ = whale._constrain_solution(original)
    assert original == [0.3, 0.7], "Original list should remain unchanged"

    # The returned type should be a list of floats
    assert isinstance(clipped, list) and all(isinstance(v, (float, int)) for v in clipped)
