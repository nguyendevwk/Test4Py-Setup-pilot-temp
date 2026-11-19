import itertools
import math
import pytest
from tqdm.contrib.itertools import permutations

def test_permutations_normal_behavior():
    """Verify that permutations returns the correct iterable and total count."""
    data = [1, 2, 3]
    r = 2
    # Compute expected permutations and total
    expected = list(itertools.permutations(data, r))
    expected_total = math.perm(len(data), r)

    # Call the function under test
    result = permutations(data, r)

    # The result should be a tqdm instance wrapping the permutations iterator
    assert hasattr(result, "iterable")
    # Consume the iterator and compare
    assert list(result) == expected
    # The total attribute should match the expected total
    assert result.total == expected_total

def test_permutations_boundary_empty_and_excess_r():
    """Test boundary cases: empty iterable and r greater than length."""
    # Empty iterable with r=0 should yield one empty tuple
    empty_result = permutations([], 0)
    assert list(empty_result) == [()]
    assert empty_result.total == 1

    # r greater than length should yield no permutations and total 0
    over_result = permutations([1, 2], 3)
    assert list(over_result) == []
    assert over_result.total == 0

def test_permutations_invalid_iterable_raises():
    """Passing a non-iterable should raise a TypeError."""
    with pytest.raises(TypeError):
        list(permutations(42))
