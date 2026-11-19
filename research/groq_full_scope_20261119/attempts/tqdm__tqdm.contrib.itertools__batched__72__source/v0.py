import itertools
import math
import pytest
from tqdm.contrib.itertools import batched
from tqdm.auto import tqdm as tqdm_auto

def test_batched_basic():
    data = list(range(10))
    n = 3
    result = batched(data, n)
    # The returned object should be a tqdm instance
    assert isinstance(result, tqdm_auto)
    # The iterator should yield batches of size n (except possibly the last)
    batches = list(result)
    assert batches == [list(range(0, 3)), list(range(3, 6)), list(range(6, 9)), list(range(9, 10))]
    # The total number of batches should be ceil(len(data)/n)
    assert result.total == math.ceil(len(data) / n)
    # unit_scale should be set to n
    assert result.unit_scale == n

def test_batched_with_total_override():
    data = list(range(5))
    n = 2
    # Override total to 10
    result = batched(data, n, total=10)
    batches = list(result)
    assert batches == [list(range(0, 2)), list(range(2, 4)), list(range(4, 5))]
    # The total should reflect the overridden value
    assert result.total == 10
    # unit_scale remains n
    assert result.unit_scale == n

def test_batched_non_len_iterable():
    # Generator has no len()
    gen = (x for x in range(4))
    n = 2
    result = batched(gen, n)
    batches = list(result)
    assert batches == [list(range(0, 2)), list(range(2, 4))]
    # Since total cannot be determined, result.total should be None
    assert result.total is None
    # unit_scale should still be n
    assert result.unit_scale == n
