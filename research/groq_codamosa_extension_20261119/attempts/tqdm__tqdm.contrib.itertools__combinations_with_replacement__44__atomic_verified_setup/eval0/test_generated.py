import itertools
import math
import pytest
from tqdm.contrib.itertools import combinations_with_replacement

def test_combinations_with_replacement_basic():
    # Basic case: iterable of 3 elements, r=2
    iterable = ['a', 'b', 'c']
    r = 2
    # Expected combinations
    expected = list(itertools.combinations_with_replacement(iterable, r))
    # Use the tqdm wrapper
    result = list(combinations_with_replacement(iterable, r))
    assert result == expected
    # Total should be precomputed correctly
    # For n=3, r=2: C(3+2-1,2)=C(4,2)=6
    assert result.tqdm.total == 6

def test_combinations_with_replacement_zero_r():
    # Boundary case: r=0 should yield one empty tuple
    iterable = [1, 2, 3]
    r = 0
    result = list(combinations_with_replacement(iterable, r))
    assert result == [()]
    # Total should be 1
    assert result.tqdm.total == 1

def test_combinations_with_replacement_invalid_iterable():
    # Error case: non-iterable input should raise TypeError
    with pytest.raises(TypeError):
        list(combinations_with_replacement(42, 2))
