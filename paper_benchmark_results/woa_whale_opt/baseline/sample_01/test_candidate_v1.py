import pytest
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clamps_bounds():
    # Dummy objective function (unused in this test)
    dummy_opt = lambda x, y: 0
    constraints = [(0.0, 1.0), (2.0, 3.0)]
    # Instantiate with arbitrary parameters
    wo = WhaleOptimization(dummy_opt, constraints, nsols=1, b=1.0, a=1.0, a_step=0.1)

    # Case 1: values outside bounds
    out_of_bounds = [-0.5, 4.0]
    constrained = wo._constrain_solution(out_of_bounds)
    assert constrained == [0.0, 3.0], "Values should be clamped to the bounds"

    # Case 2: values inside bounds (unchanged)
    inside_bounds = [0.5, 2.5]
    constrained_inside = wo._constrain_solution(inside_bounds)
    assert constrained_inside == inside_bounds, "Values inside bounds should remain unchanged"
