import numpy as np
from src.whale_optimization import WhaleOptimization

def test_whale_optimization_optimize_updates_state():
    np.random.seed(0)
    opt_func = lambda x, y: x**2 + y**2
    constraints = [(-5, 5), (-5, 5)]
    woa = WhaleOptimization(opt_func, constraints, nsols=5, b=1, a=2, a_step=0.1)
    initial_a = woa._a
    initial_sols_shape = woa._sols.shape
    woa.optimize()
    # shape of solutions remains (nsols, 2)
    assert woa._sols.shape == initial_sols_shape
    # a decreased by a_step
    assert woa._a == initial_a - woa._a_step
    # best_solutions list updated
    assert len(woa._best_solutions) == 1
    best_fitness, best_sol = woa._best_solutions[0]
    # fitness matches the minimum of current solutions
    current_fitness = opt_func(woa._sols[:, 0], woa._sols[:, 1])
    assert best_fitness == np.min(current_fitness)
    # solution is within constraints
    assert all(constraints[i][0] <= best_sol[i] <= constraints[i][1] for i in range(2))
