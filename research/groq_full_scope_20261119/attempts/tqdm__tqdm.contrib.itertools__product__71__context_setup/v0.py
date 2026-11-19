import itertools
import math
import pytest

from tqdm.contrib.itertools import product as tqdm_product


class DummyTqdm:
    """A minimal stand‑in for tqdm that records the total argument."""
    def __init__(self, iterable, total=None, **kwargs):
        self.total = total
        self.iterable = iterable

    def __iter__(self):
        return iter(self.iterable)


def test_product_normal_behavior(tmp_path):
    """Verify that product yields correct tuples and passes the expected total."""
    # Use a simple iterable pair
    a = [1, 2]
    b = ['a', 'b']
    # Call the function with a dummy tqdm class
    result = list(tqdm_product(a, b, repeat=1, tqdm_class=DummyTqdm))
    # Expected Cartesian product
    expected = list(itertools.product(a, b))
    assert result == expected
    # Total should be len(a)*len(b) = 4
    assert DummyTqdm.total == 4


def test_product_repeat_zero(tmp_path):
    """When repeat is zero, product should yield a single empty tuple."""
    # Any iterable is fine; repeat=0 should ignore it
    iterable = [1, 2, 3]
    result = list(tqdm_product(iterable, repeat=0, tqdm_class=DummyTqdm))
    # Only one tuple: the empty tuple
    assert result == [()]
    # Total should be 1 (product of zero lengths is 1)
    assert DummyTqdm.total == 1


def test_product_no_len_iterable(tmp_path):
    """If an iterable has no len, total should remain None and no exception raised."""
    # Generator has no len
    gen = (x for x in range(3))
    result = list(tqdm_product(gen, repeat=1, tqdm_class=DummyTqdm))
    # Should produce the same as itertools.product
    expected = list(itertools.product(gen))
    assert result == expected
    # Since len cannot be determined, total should be None
    assert DummyTqdm.total is None
