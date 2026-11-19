import pytest
from flutes.iterator import scanr

def test_scanr_basic_addition():
    # Normal case: sum of integers with an explicit initial value
    result = scanr(lambda acc, x: acc + x, [1, 2, 3, 4], 0)
    assert result == [10, 9, 7, 4, 0], "scanr should compute cumulative sums from the right"

def test_scanr_no_initial_empty_iterable():
    # Boundary case: empty iterable without an initial value should raise TypeError
    with pytest.raises(TypeError):
        scanr(lambda acc, x: acc + x, [])

def test_scanr_string_concatenation():
    # Normal case: concatenating strings from the right without an explicit initial value
    result = scanr(lambda acc, x: x + acc, ['a', 'b', 'c', 'd'])
    assert result == ['abcd', 'bcd', 'cd', 'd'], "scanr should concatenate strings from the right"
