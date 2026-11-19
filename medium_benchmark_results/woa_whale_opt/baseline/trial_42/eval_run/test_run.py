import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clamps_bounds():
    # Setup: constraints [0,1] for both dimensions
    constraints = [(0.0, 1.0), (0.0, 1.0)]
    # Dummy objective function (unused for this test)
    def dummy_opt(x, y): return x + y
    # Instantiate WhaleOptimization with minimal parameters
    wo = WhaleOptimization(opt_func=dummy_opt,
                           constraints=constraints,
                           nsols=1,
                           b=1.0,
                           a=1.0,
                           a_step=0.1,
                           maximize=False)

    # Test case 1: values outside bounds
    sol_outside = np.array([-0.5, 1.5])
    constrained = wo._constrain_solution(sol_outside)
    assert constrained == [0.0, 1.0], "Values should be clamped to bounds"

    # Test case 2: values within bounds remain unchanged
    sol_inside = np.array([0.3, 0.7])
    constrained_inside = wo._constrain_solution(sol_inside)
    assert constrained_inside == [0.3, 0.7], "Values within bounds should stay the same"

    # Ensure a new list is returned, not a reference to the input
    assert constrained is not sol_outside, "Returned list should be a new object"
