import itertools
import math
import pytest
from tqdm.contrib.itertools import combinations_with_replacement
from tqdm.auto import tqdm as tqdm_auto

def test_combinations_with_replacement_basic():
    # Basic case: iterable of 3 elements, r=2
    iterable = ['a', 'b', 'c']
    r = 2
    # Expected combinations
    expected = list(itertools.combinations_with_replacement(iterable, r))
    # Compute expected total manually
    n = len(iterable)
    total_expected = math.comb(n + r - 1, r)
    # Call the function
    result = combinations_with_replacement(iterable, r)
    # The result should be a tqdm instance wrapping the iterator
    assert isinstance(result, tqdm_auto)
    # The total attribute should match the expected total
    assert result.total == total_expected
    # Iterating over the result should yield the expected combinations
    assert list(result) == expected

def test_combinations_with_replacement_boundary_empty_and_zero():
    # Boundary case: empty iterable and r=0
    iterable = []
    r = 0
    # Expected combinations: one empty tuple
    expected = [()]
    # Compute expected total manually
    total_expected = 1  # math.comb(0 + 0 - 1, 0) is not defined, but algorithm yields 1
    result = combinations_with_replacement(iterable, r)
    assert isinstance(result, tqdm_auto)
    assert result.total == total_expected
    assert list(result) == expected

def test_combinations_with_replacement_invalid_iterable():
    # Error case: non-iterable input should raise TypeError
    with pytest.raises(TypeError):
        list(combinations_with_replacement(42, 2))
