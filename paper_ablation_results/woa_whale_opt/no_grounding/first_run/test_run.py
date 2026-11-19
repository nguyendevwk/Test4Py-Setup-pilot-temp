import numpy as np
from src.whale_optimization import WhaleOptimization

def test_rank_solutions_sort_and_best_solution():
    # Simple fitness: sum of coordinates
    opt_func = lambda x, y: x + y
    constraints = [(0, 10), (0, 10)]
    nsols = 3
    whale = WhaleOptimization(opt_func, constraints, nsols, b=1, a=1, a_step=0.1)

    # Manually set unsorted solutions
    whale._sols = np.array([[5, 6], [1, 2], [3, 4]])

    ranked = whale._rank_solutions()

    # Solutions should be sorted by ascending fitness (default maximize=False)
    assert [list(r) for r in ranked] == [[1, 2], [3, 4], [5, 6]]

    # Best solution should be appended to history
    best_fitness, best_sol = whale._best_solutions[-1]
    assert best_fitness == 3.0
    assert np.array_equal(best_sol, np.array([1, 2]))
