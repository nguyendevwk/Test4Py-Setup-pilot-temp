import itertools
import math
import pytest
from tqdm.contrib.itertools import permutations
from tqdm.auto import tqdm as tqdm_auto

def test_permutations_normal():
    """Test that permutations returns the correct number of tuples for a normal case."""
    data = [1, 2, 3]
    r = 2
    # Compute expected number of permutations
    expected_total = math.perm(len(data), r)
    # Use the function
    result = permutations(data, r)
    # Convert to list to exhaust the iterator
    perm_list = list(result)
    # Assert the length matches expected_total
    assert len(perm_list) == expected_total
    # Assert that each element is a tuple of length r
    for p in perm_list:
        assert isinstance(p, tuple)
        assert len(p) == r
    # Assert that all permutations are unique
    assert len(set(perm_list)) == expected_total

def test_permutations_r_greater_than_n():
    """Test that when r > n, total is set to 0 and no permutations are produced."""
    data = [1, 2]
    r = 5  # greater than len(data)
    result = permutations(data, r)
    # The iterator should be empty
    perm_list = list(result)
    assert perm_list == []
    # The total attribute of the tqdm object should be 0
    assert getattr(result, "total", None) == 0

def test_permutations_total_override():
    """Test that providing a total argument overrides the automatic calculation."""
    data = [1, 2]
    # Provide a total that does not match the actual number of permutations
    custom_total = 10
    result = permutations(data, total=custom_total)
    # The iterator should still yield the correct permutations
    perm_list = list(result)
    expected_total = math.perm(len(data), len(data))
    assert len(perm_list) == expected_total
    # The total attribute should reflect the overridden value
    assert getattr(result, "total", None) == custom_total
