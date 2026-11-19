import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clamps_values():
    # Dummy objective function (unused in this test)
    def dummy_opt(x, y):
        return np.zeros_like(x)

    # Constraints: each dimension must be between 0 and 1
    constraints = [(0.0, 1.0), (0.0, 1.0)]

    # Create WhaleOptimization instance
    wo = WhaleOptimization(opt_func=dummy_opt,
                           constraints=constraints,
                           nsols=1,
                           b=1.0,
                           a=1.0,
                           a_step=0.1,
                           maximize=False)

    # Test case: values outside bounds
    out_of_bounds = np.array([-0.5, 1.5])
    constrained = wo._constrain_solution(out_of_bounds)
    assert isinstance(constrained, list), "Result should be a list"
    assert constrained == [0.0, 1.0], "Values should be clamped to bounds"

    # Test case: values within bounds
    in_bounds = np.array([0.3, 0.7])
    constrained = wo._constrain_solution(in_bounds)
    assert constrained == [0.3, 0.7], "Values within bounds should remain unchanged"

    # Test case: values exactly on bounds
    on_bounds = np.array([0.0, 1.0])
    constrained = wo._constrain_solution(on_bounds)
    assert constrained == [0.0, 1.0], "Values on bounds should remain unchanged"
