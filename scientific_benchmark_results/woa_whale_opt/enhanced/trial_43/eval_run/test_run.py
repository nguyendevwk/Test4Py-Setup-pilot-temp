import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_optimize_updates_state_and_constraints():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=3, b=1, a=2, a_step=0.5)
    initial_a = woa._a
    initial_best_len = len(woa._best_solutions)

    woa.optimize()

    # a should be decreased by a_step
    assert woa._a == pytest.approx(initial_a - woa._a_step)

    # best solutions list should have one more entry
    assert len(woa._best_solutions) == initial_best_len + 1

    # solutions shape remains unchanged
    assert woa._sols.shape == (3, 2)

    # all solutions respect constraints
    for sol in woa._sols:
        assert all(c[0] <= val <= c[1] for val, c in zip(sol, constraints))

    # best solution fitness should be minimal (since maximize=False)
    best_fitness, best_sol = woa._best_solutions[-1]
    fitnesses = [opt_func(*s) for s in woa._sols]
    assert best_fitness == pytest.approx(min(fitnesses))
