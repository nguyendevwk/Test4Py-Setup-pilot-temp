import itertools
import math
import pytest

from tqdm.contrib.itertools import product as tqdm_product


class DummyTqdm:
    """A minimal stand‑in for tqdm that records the total argument and yields the iterable."""
    def __init__(self, iterable, total=None, **kwargs):
        self.total = total
        self.iterable = iterable

    def __iter__(self):
        return iter(self.iterable)


def test_product_normal_iterables(tmp_path):
    """Test normal behaviour with two small iterables and a custom tqdm_class."""
    a = [1, 2]
    b = ['x', 'y']
    # Use DummyTqdm to capture the total argument
    result = list(tqdm_product(a, b, tqdm_class=DummyTqdm))
    # Expected product
    expected = list(itertools.product(a, b))
    assert result == expected
    # Total should be len(a) * len(b) = 4
    assert DummyTqdm.total == 4


def test_product_repeat_zero(tmp_path):
    """When repeat=0, itertools.product yields a single empty tuple."""
    result = list(tqdm_product([1, 2, 3], repeat=0, tqdm_class=DummyTqdm))
    assert result == [()]
    # Total should be 1 (since product of zero lengths is 1)
    assert DummyTqdm.total == 1


def test_product_generator_no_len(tmp_path):
    """If an iterable has no len, total should remain None and iteration should succeed."""
    gen = (i for i in range(3))
    result = list(tqdm_product(gen, [10, 20], tqdm_class=DummyTqdm))
    expected = list(itertools.product(gen, [10, 20]))
    assert result == expected
    # Since gen has no len, total should be None
    assert DummyTqdm.total is None
