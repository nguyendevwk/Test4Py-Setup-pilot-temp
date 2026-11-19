import pytest
from flutes.iterator import scanr

def test_scanr_basic_sum():
    """Normal case: sum of integers with initial value."""
    result = scanr(lambda acc, x: acc + x, [1, 2, 3, 4], 0)
    assert result == [10, 9, 7, 4, 0]
    # Ensure the original list is unchanged
    assert [1, 2, 3, 4] == [1, 2, 3, 4]

def test_scanr_empty_iterable():
    """Boundary case: empty iterable should return a list containing only the initial value."""
    result = scanr(lambda acc, x: acc + x, [], 0)
    assert result == [0]
    # No intermediate values should be produced
    assert len(result) == 1

def test_scanr_invalid_iterable():
    """Error case: passing a non-iterable should raise a TypeError."""
    with pytest.raises(TypeError):
        scanr(lambda acc, x: acc + x, 42, 0)
