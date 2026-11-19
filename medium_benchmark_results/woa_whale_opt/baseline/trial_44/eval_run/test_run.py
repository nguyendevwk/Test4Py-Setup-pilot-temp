import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clamps_bounds():
    # Dummy objective function (not used in this test)
    def dummy_opt(x, y):
        return x + y

    # Constraints: each dimension must be between 0 and 1
    constraints = [(0.0, 1.0), (0.0, 1.0)]

    # Create WhaleOptimization instance (random init irrelevant here)
    wo = WhaleOptimization(
        opt_func=dummy_opt,
        constraints=constraints,
        nsols=1,
        b=1.0,
        a=1.0,
        a_step=0.1,
    )

    # Test values outside bounds are clamped
    out_of_bounds = np.array([-0.5, 1.5])
    constrained = wo._constrain_solution(out_of_bounds)
    assert constrained == [0.0, 1.0], "Values should be clamped to bounds"

    # Test values inside bounds remain unchanged
    in_bounds = np.array([0.3, 0.7])
    constrained = wo._constrain_solution(in_bounds)
    assert constrained == [0.3, 0.7], "Values inside bounds should remain unchanged"
