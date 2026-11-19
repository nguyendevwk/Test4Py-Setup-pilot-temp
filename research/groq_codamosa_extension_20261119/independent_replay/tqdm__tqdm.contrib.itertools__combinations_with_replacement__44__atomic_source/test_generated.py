import itertools
import math
import pytest
from tqdm.contrib.itertools import combinations_with_replacement
from tqdm.auto import tqdm as tqdm_auto

def test_combinations_with_replacement_basic():
    # Basic case: iterable of 3 elements, r=2
    iterable = [1, 2, 3]
    r = 2
    # Compute expected combinations using itertools directly
    expected = list(itertools.combinations_with_replacement(iterable, r))
    # Use the function under test
    result = combinations_with_replacement(iterable, r)
    # The result should be a tqdm instance wrapping the iterator
    assert isinstance(result, tqdm_auto)
    # Convert to list to exhaust iterator
    actual = list(result)
    assert actual == expected
    # Total should be precomputed correctly
    # For n=3, r=2: total = C(3+2-1, 2) = C(4,2) = 6
    assert result.total == 6

def test_combinations_with_replacement_zero_r():
    # Boundary case: r=0 should yield one empty tuple
    iterable = ['a', 'b', 'c']
    r = 0
    result = combinations_with_replacement(iterable, r)
    assert isinstance(result, tqdm_auto)
    actual = list(result)
    assert actual == [()]
    # Total should be 1
    assert result.total == 1

def test_combinations_with_replacement_invalid_iterable():
    # Passing a non-iterable should raise a TypeError from itertools
    non_iterable = 42  # int is not iterable
    r = 1
    with pytest.raises(TypeError):
        list(combinations_with_replacement(non_iterable, r))
