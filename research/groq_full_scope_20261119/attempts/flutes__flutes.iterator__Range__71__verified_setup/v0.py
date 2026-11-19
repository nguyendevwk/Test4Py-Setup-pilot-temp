import pytest
from flutes.iterator import Range

def test_range_iteration_and_length():
    r = Range(0, 5, 2)
    assert len(r) == 2
    assert list(r) == [0, 2]
    # Ensure that the iterator is independent of the original sequence
    it = iter(r)
    assert next(it) == 0
    assert next(it) == 2
    with pytest.raises(StopIteration):
        next(it)

def test_range_slicing_and_negative_index():
    r = Range(10, 20, 3)
    # Slice from index 1 to 3 (exclusive)
    sliced = r[1:3]
    assert sliced == [13, 16]
    # Negative index should wrap correctly
    assert r[-1] == 19
    assert r[-3] == 13

def test_invalid_initialization_raises_value_error():
    with pytest.raises(ValueError):
        Range()          # no arguments
    with pytest.raises(ValueError):
        Range(1, 2, 3, 4)  # too many arguments
