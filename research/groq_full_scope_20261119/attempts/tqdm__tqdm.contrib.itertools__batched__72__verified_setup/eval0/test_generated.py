import itertools
import math
import pytest
from tqdm.contrib.itertools import batched

def test_batched_normal_behavior():
    data = list(range(10))
    n = 3
    # Use default tqdm_auto; capture the returned tqdm iterator
    batched_iter = batched(data, n)
    # The iterator should be a tqdm instance
    assert hasattr(batched_iter, "total")
    # Total number of batches should be ceil(len(data)/n)
    expected_total = (len(data) + n - 1) // n
    assert batched_iter.total == expected_total
    # Collect batches
    batches = list(batched_iter)
    # Verify number of batches
    assert len(batches) == expected_total
    # Verify each batch size (except possibly last)
    for i, batch in enumerate(batches):
        if i < expected_total - 1:
            assert len(batch) == n
        else:
            # last batch may be smaller
            assert len(batch) == len(data) % n or len(batch) == n
    # Verify content matches original data
    assert list(itertools.chain.from_iterable(batches)) == data

def test_batched_boundary_large_n():
    data = [1, 2, 3]
    n = 10  # larger than data length
    batched_iter = batched(data, n)
    assert batched_iter.total == 1  # only one batch
    batches = list(batched_iter)
    assert len(batches) == 1
    assert batches[0] == data  # entire data in one batch

def test_batched_invalid_n_raises():
    data = [1, 2, 3]
    with pytest.raises(ValueError):
        # itertools.batched raises ValueError for non-positive n
        list(batched(data, 0))
    with pytest.raises(ValueError):
        list(batched(data, -5))
