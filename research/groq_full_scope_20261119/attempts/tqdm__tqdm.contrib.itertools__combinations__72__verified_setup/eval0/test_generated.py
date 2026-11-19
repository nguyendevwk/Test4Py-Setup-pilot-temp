import itertools
import math
import pytest

from tqdm.contrib.itertools import combinations


class DummyTqdm:
    """Simple stand‑in for tqdm that records the iterable and total."""
    def __init__(self, iterable, total=None, **kwargs):
        self.iterable = iterable
        self.total = total
        self.kwargs = kwargs

    def __iter__(self):
        return iter(self.iterable)


def test_combinations_normal():
    """Verify that total is correctly computed for a normal case."""
    iterable = [1, 2, 3]
    r = 2
    result = combinations(iterable, r, tqdm_class=DummyTqdm)
    # DummyTqdm should have captured the total as math.comb(3, 2) == 3
    assert isinstance(result, DummyTqdm)
    assert result.total == math.comb(len(iterable), r)
    # The underlying iterable should be an itertools.combinations object
    assert isinstance(result.iterable, itertools.combinations)
    # Ensure the combinations are correct
    expected = list(itertools.combinations(iterable, r))
    assert list(result) == expected


def test_combinations_r_greater_than_n():
    """When r > len(iterable), total should be 0 and no combinations produced."""
    iterable = [1, 2]
    r = 3
    result = combinations(iterable, r, tqdm_class=DummyTqdm)
    assert isinstance(result, DummyTqdm)
    assert result.total == 0
    # No combinations should be produced
    assert list(result) == []


def test_combinations_iterable_without_len():
    """If iterable has no __len__, total should remain None."""
    # Generator has no length
    iterable = (x for x in range(5))
    r = 2
    result = combinations(iterable, r, tqdm_class=DummyTqdm)
    assert isinstance(result, DummyTqdm)
    # Since len() fails, total should be None
    assert result.total is None
    # The combinations should still be correct
    expected = list(itertools.combinations(range(5), r))
    assert list(result) == expected
