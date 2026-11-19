import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clamps_bounds():
    # Arrange: create a WhaleOptimization instance with simple constraints
    opt_func = lambda x, y: x + y  # dummy objective
    constraints = [(0.0, 1.0), (0.0, 1.0)]  # bounds for two variables
    wo = WhaleOptimization(opt_func, constraints, nsols=1, b=1.0, a=1.0, a_step=0.1)

    # Act: clamp a solution that violates bounds
    out_of_bounds = [-0.5, 1.5]
    clamped = wo._constrain_solution(out_of_bounds)

    # Assert: values are clamped to the bounds
    assert clamped == [0.0, 1.0], f"Expected [0.0, 1.0], got {clamped}"

    # Act: clamp a solution that is already within bounds
    in_bounds = [0.2, 0.8]
    unchanged = wo._constrain_solution(in_bounds)

    # Assert: values remain unchanged
    assert unchanged == [0.2, 0.8], f"Expected [0.2, 0.8], got {unchanged}"
