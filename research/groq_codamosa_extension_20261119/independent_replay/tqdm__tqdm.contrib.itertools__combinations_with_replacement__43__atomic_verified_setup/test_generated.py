import itertools
import math
import pytest
from tqdm.contrib.itertools import combinations_with_replacement

def test_combinations_with_replacement_basic():
    # Basic functionality: generate combinations and verify total count
    iterable = [1, 2, 3]
    r = 2
    # Expected combinations
    expected = list(itertools.combinations_with_replacement(iterable, r))
    # Use the tqdm wrapper
    result_iter = combinations_with_replacement(iterable, r)
    result = list(result_iter)
    assert result == expected
    # The total attribute should match the number of combinations
    assert result_iter.total == len(expected)

def test_combinations_with_replacement_boundary_empty_and_zero():
    # Empty iterable with r=0 should yield one empty tuple
    iterable = []
    r = 0
    result_iter = combinations_with_replacement(iterable, r)
    result = list(result_iter)
    assert result == [()]
    assert result_iter.total == 1

    # Non-empty iterable with r=0 should also yield one empty tuple
    iterable = [1, 2, 3]
    result_iter = combinations_with_replacement(iterable, 0)
    result = list(result_iter)
    assert result == [()]
    assert result_iter.total == 1

def test_combinations_with_replacement_invalid_r():
    # Negative r should raise ValueError from itertools
    iterable = [1, 2, 3]
    with pytest.raises(ValueError):
        list(combinations_with_replacement(iterable, -1))
