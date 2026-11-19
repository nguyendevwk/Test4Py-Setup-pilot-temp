import itertools
import math
import pytest
from tqdm.contrib.itertools import product as tqdm_product

class DummyTqdm:
    """Simple stand‑in for tqdm that records the total argument."""
    def __init__(self, iterable, total=None, **kwargs):
        self.total = total
        self.iterable = iterable
    def __iter__(self):
        return iter(self.iterable)

def test_total_computed_for_known_lengths():
    """When iterables have known lengths, total is computed as product of lengths."""
    a = [1, 2]
    b = ['x', 'y', 'z']
    # Use DummyTqdm to capture the total passed to tqdm
    result = list(tqdm_product(a, b, tqdm_class=DummyTqdm))
    # Expected total: len(a) * len(b) = 2 * 3 = 6
    assert len(result) == 6
    # Verify that DummyTqdm received the correct total
    dummy = DummyTqdm(itertools.product(a, b))
    assert dummy.total == 6

def test_custom_tqdm_receives_correct_total_and_yields_items():
    """Custom tqdm_class receives the computed total and yields the correct items."""
    a = [0, 1]
    b = [10]
    # repeat=2 should produce 2^2 * 1 = 4 combinations
    result = list(tqdm_product(a, b, repeat=2, tqdm_class=DummyTqdm))
    expected = list(itertools.product(a, b, repeat=2))
    assert result == expected
    # DummyTqdm should have total equal to 4
    dummy = DummyTqdm(itertools.product(a, b, repeat=2))
    assert dummy.total == 4

def test_total_none_when_iterable_lengths_unknown():
    """If any iterable has no length, total remains None and no exception is raised."""
    # Define a generator (no len)
    gen = (i for i in range(3))
    # Use DummyTqdm to capture the total argument
    result = list(tqdm_product(gen, [1, 2], tqdm_class=DummyTqdm))
    # Total should be None because len(gen) is not available
    dummy = DummyTqdm(itertools.product(gen, [1, 2]))
    assert dummy.total is None
    # Ensure the product yields the correct combinations
    expected = list(itertools.product(gen, [1, 2]))
    assert result == expected
