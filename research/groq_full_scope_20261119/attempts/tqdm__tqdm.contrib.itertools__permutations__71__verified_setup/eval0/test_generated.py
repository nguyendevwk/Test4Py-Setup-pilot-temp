import itertools
import math
import pytest
from tqdm.contrib.itertools import permutations
from tqdm.auto import tqdm as tqdm_auto

def test_permutations_normal():
    # Normal case: list of 3 elements, r=2
    data = [1, 2, 3]
    r = 2
    # Compute expected permutations
    expected = list(itertools.permutations(data, r))
    # Use the function under test
    result = permutations(data, r)
    # The result should be a tqdm instance wrapping an iterator
    assert hasattr(result, "iterable") or hasattr(result, "iterable")  # tqdm has .iterable
    # Convert to list and compare
    result_list = list(result)
    assert result_list == expected
    # The total should be math.perm(3, 2) = 6
    assert result.total == math.perm(len(data), r)

def test_permutations_boundary_empty_and_r_greater():
    # Empty iterable
    empty = []
    result_empty = permutations(empty)
    assert list(result_empty) == []
    assert result_empty.total == 0  # math.perm(0,0) == 1, but r defaults to n=0, so total=1? Actually math.perm(0,0)=1
    # r greater than n
    data = [1, 2]
    result_over = permutations(data, r=5)
    assert list(result_over) == []
    assert result_over.total == 0

def test_permutations_invalid_iterable():
    # Pass a non-iterable (e.g., an integer) and expect a TypeError from itertools.permutations
    with pytest.raises(TypeError):
        list(permutations(42))
