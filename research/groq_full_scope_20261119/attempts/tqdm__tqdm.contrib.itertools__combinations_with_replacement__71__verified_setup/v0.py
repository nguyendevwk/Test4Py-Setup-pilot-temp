import itertools
import math
import pytest
from tqdm.contrib.itertools import combinations_with_replacement

def test_combinations_with_replacement_basic():
    # Basic test: 3 elements, r=2, expect 6 combinations
    iterable = ['a', 'b', 'c']
    r = 2
    result = list(combinations_with_replacement(iterable, r))
    expected = list(itertools.combinations_with_replacement(iterable, r))
    assert result == expected
    # Check that the total attribute is correctly computed
    # For n=3, r=2: total = C(3+2-1, 2) = C(4,2) = 6
    assert result.total == 6

def test_combinations_with_replacement_zero_r():
    # Boundary case: r=0 should yield one empty tuple
    iterable = [1, 2, 3]
    r = 0
    result = list(combinations_with_replacement(iterable, r))
    assert result == [()]
    # Total should be 1
    assert result.total == 1

def test_combinations_with_replacement_invalid_iterable():
    # Error case: iterable without length and not iterable
    class NonIterable:
        pass
    with pytest.raises(TypeError):
        list(combinations_with_replacement(NonIterable(), 2))
