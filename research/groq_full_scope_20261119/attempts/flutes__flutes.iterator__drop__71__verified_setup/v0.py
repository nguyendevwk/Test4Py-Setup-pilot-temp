import pytest
from flutes.iterator import drop

def test_drop_normal():
    # Drop first 3 elements from a list of 5
    result = list(drop(3, [10, 20, 30, 40, 50]))
    assert result == [40, 50], "Should return elements after the first 3"

def test_drop_boundary_empty_iterable():
    # Dropping from an empty iterable should yield nothing
    result = list(drop(5, []))
    assert result == [], "Dropping from empty iterable should return empty iterator"

def test_drop_negative_n_raises():
    # Negative n should raise ValueError
    with pytest.raises(ValueError) as excinfo:
        list(drop(-1, [1, 2, 3]))
    assert "`n` should be non-negative" in str(excinfo.value)
