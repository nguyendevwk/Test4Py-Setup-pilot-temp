import pytest
from flutes.iterator import take

def test_take_normal():
    """Normal case: take first 3 elements from a list."""
    result = list(take(3, [10, 20, 30, 40, 50]))
    assert result == [10, 20, 30], "Should return the first three elements"

def test_take_boundary_empty_and_short():
    """Boundary case: n larger than iterable length and n=0."""
    # n larger than length
    result_large_n = list(take(10, [1, 2, 3]))
    assert result_large_n == [1, 2, 3], "Should return all elements when n exceeds length"

    # n equal to 0
    result_zero = list(take(0, [1, 2, 3]))
    assert result_zero == [], "Should return an empty list when n is 0"

def test_take_error_negative_n():
    """Error case: negative n should raise ValueError."""
    with pytest.raises(ValueError, match="`n` should be non-negative"):
        list(take(-1, [1, 2, 3]))
