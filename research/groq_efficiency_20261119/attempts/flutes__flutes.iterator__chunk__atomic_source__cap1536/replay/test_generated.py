import pytest
from flutes.iterator import chunk

def test_chunk_normal():
    data = range(10)
    result = list(chunk(3, data))
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    # Ensure that the original iterable is not consumed prematurely
    assert list(chunk(3, data)) == result

def test_chunk_boundary_cases():
    # n equals 1: each element should be its own chunk
    assert list(chunk(1, [1, 2, 3])) == [[1], [2], [3]]
    # n larger than the iterable length: single chunk
    assert list(chunk(10, [4, 5])) == [[4, 5]]
    # Empty iterable should yield nothing
    assert list(chunk(5, [])) == []

def test_chunk_invalid_n():
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(0, [1, 2, 3]))
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(-3, [1, 2, 3]))
