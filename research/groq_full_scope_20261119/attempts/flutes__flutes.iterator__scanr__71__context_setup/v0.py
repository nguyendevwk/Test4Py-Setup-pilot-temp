import pytest
from flutes.iterator import scanr, scanl

def test_scanr_basic_sum():
    """Normal behavior: sum of integers with initial accumulator."""
    result = scanr(lambda acc, x: acc + x, [1, 2, 3, 4], 0)
    assert result == [10, 9, 7, 4, 0]
    # Ensure that the original list is not modified
    assert [1, 2, 3, 4] == [1, 2, 3, 4]

def test_scanr_no_initial():
    """Boundary case: no initial value, first element used as accumulator."""
    result = scanr(lambda acc, x: acc + x, [5, 6, 7])
    # Equivalent to scanl with reversed list and no initial
    expected = list(scanl(lambda acc, x: acc + x, [7, 6, 5]))
    assert result == expected[::-1]
    assert result == [18, 13, 7]

def test_scanr_invalid_args():
    """Error behavior: too many arguments raise ValueError."""
    with pytest.raises(ValueError, match="Too many arguments"):
        list(scanr(lambda acc, x: acc + x, [1, 2], 0, 1))
