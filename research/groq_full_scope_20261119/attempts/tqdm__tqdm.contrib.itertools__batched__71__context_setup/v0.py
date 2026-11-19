import itertools
import math
import pytest
from tqdm.contrib.itertools import batched

def test_batched_with_sequence_and_total():
    data = list(range(10))
    n = 3
    # Compute expected batches
    expected = [data[i:i+n] for i in range(0, len(data), n)]
    # Use batched and collect results
    result = list(batched(data, n))
    assert result == expected
    # Verify that the returned iterator is a tqdm instance with correct total
    # The total number of batches should be ceil(len(data)/n)
    expected_total = (len(data) + n - 1) // n
    # The tqdm object is the first element of the iterator
    tqdm_obj = result[0].__iter__().__self__
    assert tqdm_obj.total == expected_total
    assert tqdm_obj.unit_scale == n

def test_batched_with_generator_and_no_len():
    # Generator has no len
    gen = (x for x in range(5))
    n = 2
    # Expected batches
    expected = [[0,1],[2,3],[4]]
    result = list(batched(gen, n))
    assert result == expected
    # Since total is None, tqdm.total should be None
    tqdm_obj = result[0].__iter__().__self__
    assert tqdm_obj.total is None
    assert tqdm_obj.unit_scale == n

def test_batched_invalid_batch_size():
    data = [1, 2, 3]
    with pytest.raises(ValueError):
        list(batched(data, 0))
