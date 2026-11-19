import itertools
import math
import pytest
from tqdm.contrib.itertools import batched
from tqdm.auto import tqdm as tqdm_auto

def test_batched_basic_iteration_and_total():
    # Basic iteration over a range with batch size 2
    iterable = range(5)
    n = 2
    # Use default total calculation
    batched_iter = batched(iterable, n)
    # The returned object should be a tqdm instance
    assert hasattr(batched_iter, "update")
    # Convert to list to trigger iteration
    result = list(batched_iter)
    # itertools.batched yields tuples
    assert result == [(0, 1), (2, 3), (4,)]
    # The total number of batches should be ceil(5/2) = 3
    assert batched_iter.total == 3
    # The unit_scale should be set to the batch size
    assert batched_iter.unit_scale == n

def test_batched_with_explicit_total_and_kwargs():
    # Explicit total should override len-based calculation
    iterable = [1, 2, 3, 4, 5, 6]
    n = 3
    explicit_total = 4  # intentionally larger than actual length
    batched_iter = batched(iterable, n, total=explicit_total, desc="test")
    # The total should be ceil(explicit_total / n) = ceil(4/3) = 2
    assert batched_iter.total == 2
    # The description should be set
    assert batched_iter.desc == "test"
    # Iterate and check batches
    result = list(batched_iter)
    assert result == [(1, 2, 3), (4, 5, 6)]
    # The unit_scale should still be n
    assert batched_iter.unit_scale == n

def test_batched_invalid_batch_size_raises():
    # itertools.batched raises ValueError for non-positive batch sizes
    iterable = [1, 2, 3]
    with pytest.raises(ValueError):
        list(batched(iterable, 0))
    with pytest.raises(ValueError):
        list(batched(iterable, -1))
