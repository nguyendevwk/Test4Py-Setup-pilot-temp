import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_updates_state_and_constraints():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=5, b=1, a=2, a_step=0.1)

    # initial state
    assert woa._sols.shape == (5, 2)
    assert woa._a == 2

    # run first optimization
    woa.optimize()
    assert woa._a == pytest.approx(1.9)
    assert len(woa._best_solutions) == 1

    # fitness consistency
    fitness = opt_func(woa._sols[:, 0], woa._sols[:, 1])
    best_fitness, _ = woa._best_solutions[0]
    assert best_fitness == pytest.approx(fitness.min())

    # solutions within constraints
    for sol in woa._sols:
        assert all(c[0] <= val <= c[1] for val, c in zip(sol, constraints))

    # run second optimization
    woa.optimize()
    assert woa._a == pytest.approx(1.8)
    assert len(woa._best_solutions) == 2

    # best fitness still minimal
    fitness = opt_func(woa._sols[:, 0], woa._sols[:, 1])
    best_fitness, _ = woa._best_solutions[-1]
    assert best_fitness == pytest.approx(fitness.min())
