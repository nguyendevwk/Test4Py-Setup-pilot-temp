import pytest
from flutes.iterator import chunk

def test_chunk_normal_behavior():
    data = range(10)
    result = list(chunk(3, data))
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    # Ensure that the original iterable is not consumed prematurely
    assert list(chunk(3, data)) == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

def test_chunk_boundary_cases():
    # n equals 1 should return each element as a single-item list
    assert list(chunk(1, [1, 2, 3])) == [[1], [2], [3]]
    # n larger than the iterable length should return the whole iterable as one chunk
    assert list(chunk(10, [4, 5])) == [[4, 5]]
    # Empty iterable should yield nothing
    assert list(chunk(5, [])) == []

def test_chunk_invalid_n_raises_value_error():
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(0, [1, 2, 3]))
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(-3, [1, 2, 3]))
