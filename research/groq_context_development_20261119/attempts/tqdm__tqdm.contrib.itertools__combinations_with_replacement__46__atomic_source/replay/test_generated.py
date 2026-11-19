import itertools
import math
import pytest
from tqdm.contrib.itertools import combinations_with_replacement
from tqdm.auto import tqdm as tqdm_auto

def test_combinations_with_replacement_basic():
    # Basic test with a small iterable and r=2
    iterable = [1, 2, 3]
    r = 2
    # Expected combinations
    expected = list(itertools.combinations_with_replacement(iterable, r))
    # Use the function under test
    result = combinations_with_replacement(iterable, r)
    # The result should be a tqdm instance wrapping the iterator
    assert isinstance(result, tqdm_auto)
    # The total attribute should be correctly computed
    # For n=3, r=2: total = C(3+2-1, 2) = C(4,2) = 6
    assert result.total == 6
    # Iterate over the tqdm and compare to expected
    assert list(result) == expected

def test_combinations_with_replacement_boundary_empty_and_zero():
    # Boundary case: empty iterable and r=0
    iterable = []
    r = 0
    result = combinations_with_replacement(iterable, r)
    # For empty iterable and r=0, there is exactly one combination: the empty tuple
    assert isinstance(result, tqdm_auto)
    assert result.total == 1
    assert list(result) == [()]

    # Boundary case: non-empty iterable but r=0
    iterable = [1, 2, 3]
    r = 0
    result = combinations_with_replacement(iterable, r)
    assert isinstance(result, tqdm_auto)
    # For any iterable, r=0 yields one combination: empty tuple
    assert result.total == 1
    assert list(result) == [()]

def test_combinations_with_replacement_error_on_invalid_iterable():
    # Passing a non-iterable (e.g., an integer) should raise a TypeError
    with pytest.raises(TypeError):
        list(combinations_with_replacement(42, 2))
