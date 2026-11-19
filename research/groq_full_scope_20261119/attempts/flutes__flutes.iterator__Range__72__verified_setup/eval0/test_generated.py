import pytest
from flutes.iterator import Range

def test_range_iteration_and_length():
    r = Range(0, 5, 2)
    assert len(r) == 2
    assert list(r) == [0, 2]
    # Ensure that iterating again starts from the beginning
    it = iter(r)
    assert next(it) == 0
    assert next(it) == 2
    with pytest.raises(StopIteration):
        next(it)

def test_range_indexing_and_slicing():
    r = Range(1, 10, 3)
    # Positive indexing
    assert r[0] == 1
    assert r[1] == 4
    assert r[2] == 7
    # Negative indexing
    assert r[-1] == 7
    assert r[-2] == 4
    # Slicing
    assert r[0:3] == [1, 4, 7]
    assert r[1:3] == [4, 7]
    assert r[:2] == [1, 4]
    assert r[2:] == [7]
    # Slice with step
    assert r[::2] == [1, 7]
    # Empty slice
    assert r[3:3] == []

def test_range_invalid_arguments_and_out_of_bounds():
    # Wrong number of arguments
    with pytest.raises(ValueError):
        Range()
    with pytest.raises(ValueError):
        Range(1, 2, 3, 4)
    # Out of bounds indexing
    r = Range(0, 5)
    with pytest.raises(IndexError):
        _ = r[5]
    with pytest.raises(IndexError):
        _ = r[-6]
