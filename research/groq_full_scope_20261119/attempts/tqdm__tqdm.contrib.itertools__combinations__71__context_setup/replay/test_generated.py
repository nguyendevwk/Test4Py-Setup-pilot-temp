import itertools
import math
import pytest

from tqdm.contrib.itertools import combinations

# A minimal tqdm‑like class that records the iterable and the total argument
class DummyTqdm:
    def __init__(self, iterable, total=None, **kwargs):
        self.iterable = iterable
        self.total = total
        self.kwargs = kwargs

    def __iter__(self):
        return iter(self.iterable)

def test_combinations_normal():
    """Test normal case: iterable is a list, r < len, total is computed."""
    data = [1, 2, 3, 4]
    r = 2
    expected_total = math.comb(len(data), r)
    dummy = DummyTqdm
    result = combinations(data, r, tqdm_class=dummy)
    # The dummy should have stored the correct total
    assert result.total == expected_total
    # The iterable should yield the same combinations as itertools.combinations
    expected = list(itertools.combinations(data, r))
    assert list(result) == expected

def test_combinations_boundary_r_greater_than_len():
    """Test boundary case: r > len(iterable) should set total to 0."""
    data = [1, 2]
    r = 5
    dummy = DummyTqdm
    result = combinations(data, r, tqdm_class=dummy)
    # Total should be 0 because r > n
    assert result.total == 0
    # No combinations should be produced
    assert list(result) == []

def test_combinations_no_len_iterable():
    """Test case where iterable has no __len__: total remains None."""
    # Create a generator which has no length
    gen = (x for x in range(5))
    r = 3
    dummy = DummyTqdm
    result = combinations(gen, r, tqdm_class=dummy)
    # Since the generator has no length, total should be None
    assert result.total is None
    # The iterable should still produce the correct combinations
    expected = list(itertools.combinations(range(5), r))
    assert list(result) == expected
