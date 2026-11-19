import pytest
from flutes.iterator import scanr

def test_scanr_with_initial_value():
    # Normal case: list of integers with an explicit initial value
    result = scanr(lambda acc, x: acc + x, [1, 2, 3, 4], 0)
    assert result == [10, 9, 7, 4, 0]
    # Verify that the original list is not modified
    assert [1, 2, 3, 4] == [1, 2, 3, 4]

def test_scanr_without_initial_value():
    # Boundary case: list of strings without an explicit initial value
    result = scanr(lambda acc, x: x + acc, ['a', 'b', 'c', 'd'])
    assert result == ['abcd', 'bcd', 'cd', 'd']
    # The result should be a new list, not a reference to the input
    assert result is not ['abcd', 'bcd', 'cd', 'd']

def test_scanr_empty_iterable_raises():
    # Error case: empty iterable and no initial value should raise TypeError
    with pytest.raises(TypeError):
        scanr(lambda acc, x: acc + x, [])
