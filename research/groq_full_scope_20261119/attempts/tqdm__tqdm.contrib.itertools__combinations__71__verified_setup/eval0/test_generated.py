import itertools
import math
import pytest
from tqdm.contrib.itertools import combinations

def test_combinations_normal():
    """Test normal behavior with a sized iterable and r <= n."""
    data = [1, 2, 3, 4]
    r = 2
    # Expected total combinations
    expected_total = math.comb(len(data), r)
    # Get the tqdm wrapper
    t = combinations(data, r)
    # The total should be set correctly
    assert t.total == expected_total
    # Consume the iterator and verify the results
    result = list(t)
    expected = list(itertools.combinations(data, r))
    assert result == expected
    # Ensure the iterator is exhausted
    with pytest.raises(StopIteration):
        next(t)

def test_combinations_boundary_r_greater_than_n():
    """Test boundary case where r > n; total should be 0 and no items."""
    data = [1, 2]
    r = 5
    t = combinations(data, r)
    # Total should be 0 because r > n
    assert t.total == 0
    # No combinations should be produced
    assert list(t) == []

def test_combinations_total_override_and_unsizeable_iterable():
    """Test that providing a total overrides calculation and works with unsizeable iterable."""
    # Unsizeable iterable: generator
    gen = (x for x in range(5))
    # Provide an explicit total
    explicit_total = 10
    t = combinations(gen, 2, total=explicit_total)
    # Total should be the explicit value
    assert t.total == explicit_total
    # Consume and verify number of items equals explicit_total
    result = list(t)
    assert len(result) == explicit_total
    # The combinations should match the expected ones
    expected = list(itertools.combinations(range(5), 2))
    assert result == expected
