import pytest
from flutes.iterator import scanr, scanl

def test_scanr_basic_sum():
    """Normal case: sum of integers with initial accumulator."""
    result = scanr(lambda acc, x: acc + x, [1, 2, 3, 4], 0)
    assert result == [10, 9, 7, 4, 0]
    # Verify that scanl produces the reverse intermediate results
    assert scanl(lambda acc, x: acc + x, [1, 2, 3, 4], 0) == [0, 1, 3, 6, 10]

def test_scanr_no_initial():
    """Boundary case: no initial accumulator, first element used as start."""
    result = scanr(lambda acc, x: acc + x, ['a', 'b', 'c', 'd'])
    assert result == ['abcd', 'bcd', 'cd', 'd']
    # The corresponding scanl should start with 'a'
    assert scanl(lambda acc, x: acc + x, ['a', 'b', 'c', 'd']) == ['a', 'ba', 'cba', 'dcba']

def test_scanr_invalid_args():
    """Error case: too many arguments raise ValueError."""
    with pytest.raises(ValueError, match="Too many arguments"):
        list(scanr(lambda acc, x: acc + x, [1, 2], 0, 1))
