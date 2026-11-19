import itertools
import math
import pytest

# Import the target function
from tqdm.contrib.itertools import combinations

# Dummy tqdm class to capture arguments
class DummyTqdm:
    def __init__(self, iterable, total=None, **kwargs):
        self.iterable = iterable
        self.total = total
        self.kwargs = kwargs

    def __iter__(self):
        return iter(self.iterable)


def test_combinations_normal():
    """Test normal case where r <= len(iterable)."""
    data = [1, 2, 3]
    r = 2
    # Expected total combinations: C(3,2) = 3
    expected_total = math.comb(len(data), r)
    result = combinations(data, r, tqdm_class=DummyTqdm)
    # Verify that DummyTqdm was instantiated with correct total
    assert isinstance(result, DummyTqdm)
    assert result.total == expected_total
    # Verify that the iterable yields the correct combinations
    expected = list(itertools.combinations(data, r))
    assert list(result) == expected


def test_combinations_r_greater_than_n():
    """Test boundary case where r > len(iterable)."""
    data = [1, 2]
    r = 3
    # Expected total combinations: 0
    expected_total = 0
    result = combinations(data, r, tqdm_class=DummyTqdm)
    assert isinstance(result, DummyTqdm)
    assert result.total == expected_total
    # Iterable should be empty
    assert list(result) == []


def test_combinations_iterable_without_len():
    """Test case where iterable has no __len__ (e.g., generator)."""
    data = (x for x in range(5))  # generator, no len()
    r = 2
    # Since len is unavailable, total should remain None
    result = combinations(data, r, tqdm_class=DummyTqdm)
    assert isinstance(result, DummyTqdm)
    assert result.total is None
    # Iterable should still produce correct combinations
    expected = list(itertools.combinations(range(5), r))
    assert list(result) == expected
