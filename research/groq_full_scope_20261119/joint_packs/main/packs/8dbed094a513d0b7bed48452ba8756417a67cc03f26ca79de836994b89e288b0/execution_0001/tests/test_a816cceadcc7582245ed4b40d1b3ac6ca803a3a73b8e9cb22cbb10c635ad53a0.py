import pytest
from flutes.iterator import chunk

def test_chunk_normal_behavior():
    # Normal case: split a range into chunks of size 3
    result = list(chunk(3, range(10)))
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    # Ensure the last chunk is smaller when not divisible
    assert len(result[-1]) == 1
    assert result[-1] == [9]

def test_chunk_boundary_n_equals_one():
    # Boundary case: n == 1 should yield each element as a single-item list
    data = ['a', 'b', 'c']
    result = list(chunk(1, data))
    assert result == [['a'], ['b'], ['c']]
    # Verify that the original iterable is not modified
    assert data == ['a', 'b', 'c']

def test_chunk_invalid_n_raises_value_error():
    # Error case: n must be positive
    with pytest.raises(ValueError) as excinfo:
        list(chunk(0, [1, 2, 3]))
    assert "`n` should be positive" in str(excinfo.value)

    with pytest.raises(ValueError):
        list(chunk(-5, [1, 2, 3]))
