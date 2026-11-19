import itertools
import math
import pytest
from tqdm.contrib.itertools import chain
from tqdm.auto import tqdm as tqdm_auto

def test_chain_with_known_totals():
    """Chain two lists and verify the total is the sum of their lengths."""
    a = [1, 2, 3]
    b = [4, 5]
    # Use default tqdm_class; it should compute total automatically
    result = chain(a, b)
    # The returned object is a tqdm instance wrapping an iterator
    assert isinstance(result, tqdm_auto)
    # The total attribute should equal len(a) + len(b)
    assert result.total == len(a) + len(b)
    # Iterating over the chain yields the concatenated elements
    assert list(result) == a + b

def test_chain_with_empty_iterables():
    """Chain empty iterables and ensure total is zero and iteration yields nothing."""
    result = chain([], [])
    assert isinstance(result, tqdm_auto)
    # Total should be zero because sum of lengths of empty lists is zero
    assert result.total == 0
    # Iterating over the chain yields an empty list
    assert list(result) == []

def test_chain_with_non_len_iterables_and_total_none():
    """When iterables lack __len__, total should remain None and iteration works."""
    # Create generators which do not support len()
    gen1 = (x for x in range(3))
    gen2 = (x for x in range(2))
    result = chain(gen1, gen2)
    assert isinstance(result, tqdm_auto)
    # Since generators have no len, total should be None
    assert result.total is None
    # Iteration should produce the combined sequence
    assert list(result) == list(range(5))
