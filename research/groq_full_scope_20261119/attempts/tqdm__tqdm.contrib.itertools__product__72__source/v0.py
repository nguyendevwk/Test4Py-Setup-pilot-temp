import itertools
import math
import pytest
from tqdm.contrib.itertools import product as tqdm_product

def test_product_basic_and_total_computation():
    # Use a custom tqdm_class that simply records the total passed to it
    class DummyTqdm:
        def __init__(self, iterable, total=None, **kwargs):
            self.iterable = iterable
            self.total = total
            self.kwargs = kwargs
        def __iter__(self):
            return iter(self.iterable)

    # Two small iterables
    a = [1, 2]
    b = ['x', 'y']
    # Expected product
    expected = list(itertools.product(a, b))
    # Call the tqdm_product with our dummy tqdm_class
    result = list(tqdm_product(a, b, tqdm_class=DummyTqdm))
    assert result == expected
    # Total should be len(a)*len(b) = 4
    assert DummyTqdm.total == 4

def test_product_repeat_and_total_override():
    # Use a dummy tqdm_class that records the total
    class DummyTqdm:
        def __init__(self, iterable, total=None, **kwargs):
            self.iterable = iterable
            self.total = total
        def __iter__(self):
            return iter(self.iterable)

    # Repeat 2 times over a single iterable
    iterable = [0, 1]
    # Expected product with repeat=2
    expected = list(itertools.product(iterable, repeat=2))
    # Compute total manually: len(iterable)**repeat = 2**2 = 4
    result = list(tqdm_product(iterable, repeat=2, tqdm_class=DummyTqdm))
    assert result == expected
    assert DummyTqdm.total == 4

def test_product_with_non_iterable_raises():
    # Passing a non-iterable (int) should raise a TypeError from itertools.product
    with pytest.raises(TypeError):
        list(tqdm_product(5, [1, 2]))
