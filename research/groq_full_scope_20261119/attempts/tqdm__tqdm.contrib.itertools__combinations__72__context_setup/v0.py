import itertools
import math
import pytest

# Import the target function
from tqdm.contrib.itertools import combinations

# Dummy tqdm class to capture initialization arguments
class DummyTqdm:
    def __init__(self, iterable, total=None, **kwargs):
        self.iterable = iterable
        self.total = total
        self.kwargs = kwargs

    def __iter__(self):
        return iter(self.iterable)


def test_combinations_normal_behavior():
    """Test that combinations returns the correct iterable and total for a normal case."""
    data = [1, 2, 3, 4]
    r = 2
    # Compute expected total using math.comb
    expected_total = math.comb(len(data), r)
    # Call the function with DummyTqdm
    result = combinations(data, r, tqdm_class=DummyTqdm)
    # Verify that the returned object is an instance of DummyTqdm
    assert isinstance(result, DummyTqdm)
    # Verify that the total attribute is correctly set
    assert result.total == expected_total
    # Verify that the iterable yields the expected combinations
    expected_combinations = list(itertools.combinations(data, r))
    assert list(result) == expected_combinations


def test_combinations_boundary_r_greater_than_n():
    """Test that when r > n, total is set to 0 and the iterable is empty."""
    data = [1, 2]
    r = 5  # r greater than length of data
    result = combinations(data, r, tqdm_class=DummyTqdm)
    # Total should be 0
    assert result.total == 0
    # Iterable should be empty
    assert list(result) == []


def test_combinations_iterable_without_len():
    """Test that when the iterable has no __len__, total remains None."""
    # Create a generator which does not support len()
    gen = (x for x in range(5))
    r = 3
    result = combinations(gen, r, tqdm_class=DummyTqdm)
    # Total should be None because len() is not available
    assert result.total is None
    # Iterable should produce the same combinations as itertools.combinations
    expected = list(itertools.combinations(gen, r))
    assert list(result) == expected
