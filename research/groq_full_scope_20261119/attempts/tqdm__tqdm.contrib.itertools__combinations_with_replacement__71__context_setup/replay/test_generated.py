import itertools
import math
import pytest
from tqdm.contrib.itertools import combinations_with_replacement

def test_combinations_with_replacement_normal():
    # Normal case: list of two elements, r=2
    iterable = [1, 2]
    r = 2
    # Expected combinations: (1,1), (1,2), (2,2)
    expected = list(itertools.combinations_with_replacement(iterable, r))
    # Use the function under test
    result = combinations_with_replacement(iterable, r)
    # Convert tqdm iterator to list
    actual = list(result)
    assert actual == expected
    # Total should be 3 (computed combinatorially)
    assert result.total == 3

def test_combinations_with_replacement_boundary():
    # Boundary case: r=0 should yield one empty tuple
    iterable = [1, 2, 3]
    r = 0
    expected = [()]
    result = combinations_with_replacement(iterable, r)
    actual = list(result)
    assert actual == expected
    # Total should be 1
    assert result.total == 1

def test_combinations_with_replacement_error():
    # Error case: non-iterable input should raise TypeError
    iterable = None  # not iterable
    r = 2
    with pytest.raises(TypeError):
        list(combinations_with_replacement(iterable, r))
