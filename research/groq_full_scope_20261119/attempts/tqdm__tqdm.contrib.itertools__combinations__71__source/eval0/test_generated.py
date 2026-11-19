import itertools
import math
import pytest

from tqdm.contrib.itertools import combinations as tqdm_combinations


class DummyTqdm:
    """Simple stand‑in for tqdm that records the iterable and total."""
    def __init__(self, iterable, total=None, **kwargs):
        self.iterable = iterable
        self.total = total
        self.kwargs = kwargs

    def __iter__(self):
        return iter(self.iterable)


def test_combinations_normal():
    """Verify that combinations returns the correct items and total for a normal case."""
    data = [1, 2, 3, 4]
    r = 2
    # Use DummyTqdm to capture the total argument
    result = tqdm_combinations(data, r, tqdm_class=DummyTqdm)
    # The DummyTqdm instance should have the correct total
    assert result.total == math.comb(len(data), r)
    # The iterable should produce the expected combinations
    expected = list(itertools.combinations(data, r))
    assert list(result) == expected


def test_combinations_r_greater_than_len():
    """When r is greater than the length of the iterable, total should be 0."""
    data = [1, 2]
    r = 3
    result = tqdm_combinations(data, r, tqdm_class=DummyTqdm)
    # Total should be set to 0
    assert result.total == 0
    # No combinations should be produced
    assert list(result) == []


def test_combinations_iterable_without_len():
    """If the iterable has no __len__, total should remain None."""
    # Generator has no __len__
    data = (x for x in range(5))
    r = 2
    result = tqdm_combinations(data, r, tqdm_class=DummyTqdm)
    # Total should be None because len() is not available
    assert result.total is None
    # The iterable should still produce the correct combinations
    expected = list(itertools.combinations(range(5), r))
    assert list(result) == expected
