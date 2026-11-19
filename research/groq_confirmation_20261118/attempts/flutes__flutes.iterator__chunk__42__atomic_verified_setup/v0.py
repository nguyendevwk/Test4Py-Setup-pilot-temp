import pytest
from flutes.iterator import chunk

def test_chunk_normal():
    """Verify that chunk splits a range into correct sized groups."""
    data = list(range(10))
    result = list(chunk(3, data))
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    # Ensure original data is unchanged
    assert data == list(range(10))

def test_chunk_boundary_cases():
    """Test edge cases: n=1 and n larger than iterable length."""
    # n=1 should return each element in its own list
    data = [5, 6, 7]
    result = list(chunk(1, data))
    assert result == [[5], [6], [7]]
    # n larger than length should return the whole iterable as one chunk
    result = list(chunk(10, data))
    assert result == [data]
    # Empty iterable should yield nothing
    assert list(chunk(3, [])) == []

def test_chunk_invalid_n():
    """Chunk should raise ValueError when n is not positive."""
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(0, [1, 2, 3]))
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(-5, [1, 2, 3]))
