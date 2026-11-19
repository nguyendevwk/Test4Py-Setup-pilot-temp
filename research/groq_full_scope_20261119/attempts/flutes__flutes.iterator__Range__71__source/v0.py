import pytest
from flutes.iterator import Range

def test_range_iteration_and_length():
    r = Range(0, 5, 2)  # should produce 0,2,4
    assert len(r) == 3
    assert list(r) == [0, 2, 4]
    # Ensure that iterating again starts from the beginning
    it = iter(r)
    assert next(it) == 0
    assert next(it) == 2
    assert next(it) == 4
    with pytest.raises(StopIteration):
        next(it)

def test_range_slicing_and_negative_index():
    r = Range(10, 20, 3)  # 10,13,16,19
    # slice from index 1 to 3 (exclusive)
    assert r[1:3] == [13, 16]
    # slice with step
    assert r[::2] == [10, 16]
    # negative indexing
    assert r[-1] == 19
    assert r[-3] == 13

def test_range_invalid_initialization():
    with pytest.raises(ValueError):
        Range()          # no arguments
    with pytest.raises(ValueError):
        Range(1, 2, 3, 4)  # too many arguments
