import itertools
import math
import pytest
from tqdm.contrib.itertools import permutations

# Dummy tqdm class to capture the total argument without side effects
class DummyTqdm:
    def __init__(self, iterable, total=None, **kwargs):
        self.iterable = iterable
        self.total = total
        self.kwargs = kwargs

    def __iter__(self):
        return iter(self.iterable)

def test_permutations_normal_and_total_computed():
    """Test normal case: iterable of length 3, r=2, total should be 6."""
    data = [1, 2, 3]
    # Use dummy tqdm to capture total
    result = permutations(data, r=2, tqdm_class=DummyTqdm)
    # The dummy tqdm should have stored the correct total
    assert isinstance(result, DummyTqdm)
    assert result.total == math.perm(len(data), 2)  # 3P2 = 6
    # Verify that the iterator yields the correct permutations
    expected = list(itertools.permutations(data, 2))
    assert list(result) == expected

def test_permutations_boundary_r_greater_than_n():
    """Test boundary case: r > len(iterable) should set total to 0."""
    data = [1, 2]
    # r=3 > len(data)=2
    result = permutations(data, r=3, tqdm_class=DummyTqdm)
    assert isinstance(result, DummyTqdm)
    # Total should be 0 as per implementation
    assert result.total == 0
    # Iterator should be empty
    assert list(result) == []

def test_permutations_generator_no_length():
    """Test error-like case: iterable without __len__ should not compute total."""
    # Generator has no length
    gen = (x for x in range(4))
    result = permutations(gen, r=2, tqdm_class=DummyTqdm)
    assert isinstance(result, DummyTqdm)
    # Since total cannot be computed, it should remain None
    assert result.total is None
    # The iterator should produce the correct permutations
    expected = list(itertools.permutations(range(4), 2))
    assert list(result) == expected
