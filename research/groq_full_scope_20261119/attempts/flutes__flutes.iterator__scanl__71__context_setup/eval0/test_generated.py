import pytest
from flutes.iterator import scanl

def test_scanl_with_initial_value():
    # Normal case: provide an explicit initial accumulator
    result = list(scanl(lambda acc, x: acc + x, [1, 2, 3], 0))
    assert result == [0, 1, 3, 6]  # 0, 0+1, 1+2, 3+3

def test_scanl_without_initial_value():
    # Boundary case: no initial value, first element is used as accumulator
    result = list(scanl(lambda acc, x: acc * x, [2, 3, 4]))
    assert result == [2, 6, 24]  # 2, 2*3, 6*4

def test_scanl_invalid_arguments():
    # Error case: too many arguments should raise ValueError
    with pytest.raises(ValueError, match="Too many arguments"):
        list(scanl(lambda acc, x: acc + x, [1, 2], 0, 1))
