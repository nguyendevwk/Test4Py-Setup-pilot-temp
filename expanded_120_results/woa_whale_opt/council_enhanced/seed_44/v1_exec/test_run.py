import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_state_transition_and_constraints():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=3, b=1, a=2, a_step=0.1)

    # Record initial state
    initial_a = woa._a
    initial_best_len = len(woa._best_solutions)

    # Run one optimization step
    woa.optimize()

    # After optimization, _a should have decreased by a_step
    assert woa._a == pytest.approx(initial_a - woa._a_step)

    # _best_solutions should have one new entry
    assert len(woa._best_solutions) == initial_best_len + 1

    # Solutions array shape should remain (nsols, 2)
    assert woa._sols.shape == (3, 2)

    # All solutions must respect constraints
    for sol in woa._sols:
        assert all(constraints[i][0] <= sol[i] <= constraints[i][1] for i in range(2))

    # The best solution stored should match the best fitness in current solutions
    best_fitness, best_sol = woa._best_solutions[-1]
    computed_fitness = opt_func(best_sol[0], best_sol[1])
    assert best_fitness == pytest.approx(computed_fitness)
