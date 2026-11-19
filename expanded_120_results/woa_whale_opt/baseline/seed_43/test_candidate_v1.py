import numpy as np
import pytest
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_updates_state():
    # deterministic random numbers
    np.random.seed(0)

    # simple objective: minimize sum of squares
    def opt_func(x, y):
        return x**2 + y**2

    constraints = [[-5, 5], [-5, 5]]
    nsols = 4
    b, a, a_step = 1.0, 2.0, 0.5

    wo = WhaleOptimization(opt_func, constraints, nsols, b, a, a_step, maximize=False)

    # initial state checks
    sols_before = wo.get_solutions()
    assert sols_before.shape == (nsols, 2)
    a_before = wo._a

    # run one optimization step
    wo.optimize()

    # solutions shape unchanged
    sols_after = wo.get_solutions()
    assert sols_after.shape == (nsols, 2)

    # a decreased by a_step
    assert wo._a == pytest.approx(a_before - a_step)

    # best_solutions updated
    assert len(wo._best_solutions) == 1
    best_fitness, best_sol = wo._best_solutions[0]
    # compute fitness of all solutions after optimization
    fitness_after = opt_func(sols_after[:, 0], sols_after[:, 1])
    assert best_fitness == pytest.approx(fitness_after.min())
    # best solution matches the one with minimal fitness
    assert np.allclose(best_sol, sols_after[fitness_after.argmin()])
