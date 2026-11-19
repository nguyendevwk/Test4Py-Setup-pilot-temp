import itertools
import math
import pytest
from tqdm.contrib.itertools import chain
from tqdm.auto import tqdm as tqdm_auto

def test_chain_with_known_lengths_and_total():
    """Chain should correctly iterate over multiple iterables and set total when lengths are known."""
    a = [1, 2, 3]
    b = (4, 5)
    c = [6]
    # total should be sum of lengths
    t = chain(a, b, c)
    # The returned object is a tqdm instance
    assert isinstance(t, tqdm_auto)
    # The total attribute should equal the sum of lengths
    assert t.total == len(a) + len(b) + len(c)
    # Iterating over t yields the concatenated sequence
    assert list(t) == [1, 2, 3, 4, 5, 6]

def test_chain_with_empty_iterables_and_explicit_total():
    """Chain should handle empty iterables and respect an explicit total argument."""
    a = []
    b = []
    # Provide an explicit total that differs from the sum of lengths
    t = chain(a, b, total=10)
    assert isinstance(t, tqdm_auto)
    # The total should be the explicit value
    assert t.total == 10
    # Iterating over t yields an empty list
    assert list(t) == []

def test_chain_with_unmeasurable_iterables_and_no_total():
    """When iterables have no __len__, total should remain None if not provided."""
    # Create an iterator that does not support len()
    class NoLenIterable:
        def __iter__(self):
            return iter([7, 8, 9])
    a = NoLenIterable()
    b = NoLenIterable()
    t = chain(a, b)
    assert isinstance(t, tqdm_auto)
    # Since lengths cannot be determined, total should be None
    assert t.total is None
    # Iterating over t yields the concatenated sequence
    assert list(t) == [7, 8, 9, 7, 8, 9]
