import itertools
import math
import pytest

from tqdm.contrib.itertools import permutations
from tqdm.auto import tqdm as tqdm_auto


def test_permutations_normal_behavior():
    """Test that permutations returns correct items and total for a normal case."""
    iterable = [1, 2, 3]
    r = 2
    # Expected total permutations: P(3,2) = 6
    expected_total = math.perm(len(iterable), r)
    result = permutations(iterable, r, tqdm_class=tqdm_auto)
    # The returned object should be a tqdm instance with the correct total
    assert isinstance(result, tqdm_auto)
    assert result.total == expected_total
    # Convert to list and compare with itertools.permutations
    expected_items = list(itertools.permutations(iterable, r))
    actual_items = list(result)
    assert actual_items == expected_items
    # Ensure that the length matches the total
    assert len(actual_items) == expected_total


def test_permutations_boundary_empty_and_r_greater_than_n():
    """Test boundary cases: empty iterable and r greater than n."""
    # Empty iterable with r=0 should yield one empty tuple
    empty_iterable = []
    result_empty = permutations(empty_iterable, r=0, tqdm_class=tqdm_auto)
    assert isinstance(result_empty, tqdm_auto)
    assert result_empty.total == 1
    assert list(result_empty) == [()]

    # r greater than n should yield no permutations and total=0
    single_iterable = [42]
    result_none = permutations(single_iterable, r=2, tqdm_class=tqdm_auto)
    assert isinstance(result_none, tqdm_auto)
    assert result_none.total == 0
    assert list(result_none) == []


def test_permutations_invalid_iterable_raises_type_error():
    """Test that passing a non-iterable raises a TypeError."""
    non_iterable = 123  # int is not iterable
    with pytest.raises(TypeError):
        # itertools.permutations will raise TypeError when the input is not iterable
        list(permutations(non_iterable, r=1, tqdm_class=tqdm_auto))
