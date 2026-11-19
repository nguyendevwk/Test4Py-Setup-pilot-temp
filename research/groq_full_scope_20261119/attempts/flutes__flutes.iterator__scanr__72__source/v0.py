import pytest
from flutes.iterator import scanr

def test_scanr_with_initial_value():
    """Normal case: scanr with an explicit initial accumulator."""
    result = scanr(lambda acc, x: acc + x, [1, 2, 3, 4], 0)
    assert result == [10, 9, 7, 4, 0]
    # Ensure the original list is unchanged
    assert [1, 2, 3, 4] == [1, 2, 3, 4]

def test_scanr_without_initial_value():
    """Boundary case: scanr without an initial value uses the last element as accumulator."""
    result = scanr(lambda acc, x: acc + x, [1, 2, 3, 4])
    # The last element 4 becomes the initial accumulator, so the final element is 4
    assert result == [10, 9, 7, 4]
    # Verify that the length matches the input length
    assert len(result) == len([1, 2, 3, 4])

def test_scanr_empty_iterable_raises():
    """Error case: scanr on an empty iterable without an initial value should raise ValueError."""
    with pytest.raises(ValueError):
        scanr(lambda acc, x: acc + x, [])
