import pytest
from flutes.iterator import chunk

def test_chunk_normal_behavior():
    # Normal case: split a range into chunks of size 3
    result = list(chunk(3, range(10)))
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    # Ensure that the last chunk is smaller when the total is not a multiple of n
    assert len(result[-1]) == 1
    assert result[-1] == [9]

def test_chunk_boundary_cases():
    # n equal to 1 should return each element as a single-item list
    single = list(chunk(1, [10, 20, 30]))
    assert single == [[10], [20], [30]]
    # n larger than the iterable length should return the whole iterable as one chunk
    large_n = list(chunk(100, [1, 2, 3]))
    assert large_n == [[1, 2, 3]]
    # Empty iterable should yield nothing
    empty = list(chunk(5, []))
    assert empty == []

def test_chunk_invalid_n_raises():
    # n must be positive; zero or negative should raise ValueError
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(0, [1, 2, 3]))
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(-5, [1, 2, 3]))
