import itertools
import math
import pytest
from tqdm.contrib.itertools import combinations_with_replacement

def test_combinations_with_replacement_basic():
    # Basic functionality: iterate over combinations and check total count
    iterable = [1, 2, 3]
    r = 2
    # Expected combinations
    expected = list(itertools.combinations_with_replacement(iterable, r))
    # Use the tqdm wrapper
    result = list(combinations_with_replacement(iterable, r))
    assert result == expected
    # The tqdm wrapper should have the correct total attribute
    # The total is the number of combinations: C(n+r-1, r)
    n = len(iterable)
    expected_total = math.comb(n + r - 1, r)
    # Retrieve the tqdm object from the iterator
    # Since we consumed it, we need to recreate to inspect total
    tqdm_iter = combinations_with_replacement(iterable, r)
    assert tqdm_iter.total == expected_total

def test_combinations_with_replacement_boundary_empty_and_zero():
    # Boundary case: empty iterable and r=0
    iterable = []
    r = 0
    # itertools.combinations_with_replacement([], 0) yields one empty tuple
    expected = [()]
    result = list(combinations_with_replacement(iterable, r))
    assert result == expected
    # Total should be 1
    tqdm_iter = combinations_with_replacement(iterable, r)
    assert tqdm_iter.total == 1

    # Another boundary: non-empty iterable with r=0
    iterable = [1, 2, 3]
    r = 0
    expected = [()]
    result = list(combinations_with_replacement(iterable, r))
    assert result == expected
    tqdm_iter = combinations_with_replacement(iterable, r)
    assert tqdm_iter.total == 1

def test_combinations_with_replacement_invalid_r():
    # Negative r should raise ValueError from itertools
    iterable = [1, 2, 3]
    r = -1
    with pytest.raises(ValueError):
        list(combinations_with_replacement(iterable, r))
