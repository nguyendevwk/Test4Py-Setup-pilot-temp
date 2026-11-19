import itertools
import math
import pytest
from tqdm.contrib.itertools import combinations_with_replacement

# Helper to consume the iterator and return a list of tuples
def list_combinations(iterable, r, **kwargs):
    return list(combinations_with_replacement(iterable, r, **kwargs))

def test_normal_combinations_with_replacement():
    # Test a typical case with a small iterable and r=2
    iterable = [1, 2, 3]
    r = 2
    # Disable progress bar output
    result = list_combinations(iterable, r, disable=True)
    expected = list(itertools.combinations_with_replacement(iterable, r))
    assert result == expected
    # Verify that the total count matches the combinatorial formula
    n = len(iterable)
    total_expected = math.comb(n + r - 1, r)
    # The tqdm object is returned by the function; we can inspect its total attribute
    # by accessing the first element of the iterator (which is a tqdm instance)
    # Since we used list_combinations, we cannot access it directly; instead
    # we call the function without consuming to get the tqdm wrapper
    tqdm_iter = combinations_with_replacement(iterable, r, disable=True)
    assert tqdm_iter.total == total_expected

def test_boundary_empty_iterable_and_zero_r():
    # When iterable is empty and r=0, combinations_with_replacement should yield one empty tuple
    iterable = []
    r = 0
    result = list_combinations(iterable, r, disable=True)
    assert result == [()]
    # Total should be 1 (one combination)
    tqdm_iter = combinations_with_replacement(iterable, r, disable=True)
    assert tqdm_iter.total == 1

def test_error_non_iterable_input():
    # Passing a non-iterable (e.g., an integer) should raise a TypeError when the iterator is consumed
    iterable = 42
    r = 1
    with pytest.raises(TypeError):
        # The error occurs when itertools.combinations_with_replacement tries to iterate over the input
        list_combinations(iterable, r, disable=True)
