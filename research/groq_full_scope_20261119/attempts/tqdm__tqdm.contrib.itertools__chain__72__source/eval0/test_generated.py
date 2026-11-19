import itertools
import math
import pytest
from tqdm.contrib.itertools import chain
from tqdm.auto import tqdm as tqdm_auto

def test_chain_with_known_totals_and_lengths():
    """Chain two lists with an explicit total and verify the result and total attribute."""
    a = [1, 2]
    b = [3, 4]
    total = 4
    result = chain(a, b, total=total, desc="test")
    # The returned object should be a tqdm instance
    assert isinstance(result, tqdm_auto)
    # The total attribute should match the provided total
    assert result.total == total
    # Iterating over the result should yield the concatenated elements
    assert list(result) == [1, 2, 3, 4]

def test_chain_with_no_iterables_returns_empty():
    """Chain with no iterables should produce an empty iterator."""
    result = chain()
    # The returned object should be a tqdm instance
    assert isinstance(result, tqdm_auto)
    # The total should be None (unknown)
    assert result.total is None
    # Iterating over the result should yield nothing
    assert list(result) == []

def test_chain_with_generator_without_len():
    """Chain with a generator that has no __len__ should still work and compute total if possible."""
    gen = (x for x in range(5))
    # No total provided; chain should attempt to compute total but fail gracefully
    result = chain(gen, total=None, desc="gen")
    # The returned object should be a tqdm instance
    assert isinstance(result, tqdm_auto)
    # Since the generator has no len, total should remain None
    assert result.total is None
    # Iterating over the result should yield the generator's values
    assert list(result) == [0, 1, 2, 3, 4]
