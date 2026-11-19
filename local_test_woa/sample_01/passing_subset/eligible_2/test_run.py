import pytest
from src.whale_optimization import WhaleOptimization

def test_constrain_solution_clamps_values():
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(
        opt_func=lambda x: x[0] + x[1],
        constraints=constraints,
        nsols=1,
        b=1,
        a=2,
        a_step=0.1
    )
    # Out-of-bounds values should be clamped to the constraint limits
    out_of_bounds = [10, -10]
    assert woa._constrain_solution(out_of_bounds) == [5, -5]

    # In-bounds values should remain unchanged
    in_bounds = [-3, 4]
    assert woa._constrain_solution(in_bounds) == in_bounds
