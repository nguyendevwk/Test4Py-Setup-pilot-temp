import itertools
import math
import pytest
from tqdm.contrib.itertools import permutations

def test_permutations_normal():
    """Verify that permutations returns the correct number of items and total."""
    data = [1, 2, 3]
    # r defaults to len(data)
    result = permutations(data)
    # Consume all permutations
    perm_list = list(result)
    # There should be 3! = 6 permutations
    assert len(perm_list) == 6
    # The total attribute should be set correctly
    assert result.total == math.perm(len(data), len(data))
    # Each permutation should be a tuple of length 3
    for p in perm_list:
        assert isinstance(p, tuple)
        assert len(p) == 3

def test_permutations_r_greater_than_n():
    """When r > n, total should be 0 and no permutations are produced."""
    data = [1, 2]
    result = permutations(data, r=5)
    # No permutations should be generated
    perm_list = list(result)
    assert perm_list == []
    # Total should be set to 0
    assert result.total == 0

def test_permutations_invalid_r():
    """Providing a negative r should raise a ValueError from itertools.permutations."""
    data = [1, 2, 3]
    with pytest.raises(ValueError):
        list(permutations(data, r=-1))
