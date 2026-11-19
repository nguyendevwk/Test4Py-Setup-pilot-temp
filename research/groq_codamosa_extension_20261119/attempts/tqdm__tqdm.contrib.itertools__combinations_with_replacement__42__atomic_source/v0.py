import itertools
import math
import pytest
from tqdm.contrib.itertools import combinations_with_replacement

def test_combinations_with_replacement_basic():
    # Basic functionality: compare with itertools.combinations_with_replacement
    data = ['a', 'b', 'c']
    r = 2
    expected = list(itertools.combinations_with_replacement(data, r))
    result = list(combinations_with_replacement(data, r))
    assert result == expected
    # Ensure total is correctly computed
    # total = C(n+r-1, r) where n = len(data)
    n = len(data)
    total_expected = math.comb(n + r - 1, r)
    # The tqdm wrapper stores total in its attribute
    assert result[0].__dict__.get('total', None) == total_expected

def test_combinations_with_replacement_boundary():
    # Boundary case: empty iterable and r=0 should yield one empty tuple
    data = []
    r = 0
    result = list(combinations_with_replacement(data, r))
    assert result == [()]
    # total should be 1
    assert result[0].__dict__.get('total', None) == 1

def test_combinations_with_replacement_error():
    # Negative r should raise ValueError from itertools
    data = [1, 2, 3]
    r = -1
    with pytest.raises(ValueError):
        list(combinations_with_replacement(data, r))
