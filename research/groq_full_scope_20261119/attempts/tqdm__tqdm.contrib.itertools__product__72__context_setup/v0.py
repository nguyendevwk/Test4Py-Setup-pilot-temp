import itertools
import math
import pytest

from tqdm.contrib.itertools import product as tqdm_product


class DummyTqdm:
    """A minimal tqdm replacement that records the parameters and yields the iterable."""
    def __init__(self, iterable, total=None, **kwargs):
        self.iterable = iterable
        self.total = total
        self.kwargs = kwargs

    def __iter__(self):
        return iter(self.iterable)


def test_product_normal_behavior(tmp_path):
    """Verify that product yields the same results as itertools.product and passes the correct total."""
    a = [1, 2]
    b = ['a', 'b']
    expected = list(itertools.product(a, b))
    dummy = DummyTqdm
    result = list(tqdm_product(a, b, tqdm_class=dummy))
    assert result == expected
    # The dummy should have received the correct total: 2 * 2 = 4
    assert dummy.total == 4


def test_product_repeat_zero_boundary(tmp_path):
    """When repeat=0, product should yield a single empty tuple and total should be 1."""
    dummy = DummyTqdm
    result = list(tqdm_product([], repeat=0, tqdm_class=dummy))
    assert result == [()]
    # For an empty iterable, math.prod([]) == 1, so total = 1**0 = 1
    assert dummy.total == 1


def test_product_non_len_iterable_error(tmp_path):
    """If an iterable has no len, total should remain None and product should still work."""
    gen = (i for i in range(3))
    dummy = DummyTqdm
    result = list(tqdm_product(gen, tqdm_class=dummy))
    expected = list(itertools.product(gen))
    assert result == expected
    # Since len(gen) raises, total should be None
    assert dummy.total is None
