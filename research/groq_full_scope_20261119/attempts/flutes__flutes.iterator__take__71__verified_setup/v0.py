import pytest
from flutes.iterator import take

def test_take_normal():
    """Take should return the first n elements from a finite iterable."""
    result = list(take(3, [10, 20, 30, 40, 50]))
    assert result == [10, 20, 30], "Expected first three elements"

def test_take_boundary_empty_and_short():
    """Take should handle empty iterable and n larger than iterable length."""
    # Empty iterable
    assert list(take(5, [])) == [], "Expected empty list for empty iterable"

    # n larger than iterable length
    assert list(take(10, [1, 2])) == [1, 2], "Expected all elements when n exceeds length"

def test_take_error_negative_n():
    """Take should raise ValueError when n is negative."""
    with pytest.raises(ValueError, match="`n` should be non-negative"):
        list(take(-1, [1, 2, 3]))
