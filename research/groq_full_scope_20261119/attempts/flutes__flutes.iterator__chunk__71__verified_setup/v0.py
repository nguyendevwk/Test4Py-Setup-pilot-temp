import pytest
from flutes.iterator import chunk

def test_chunk_normal():
    """Verify that chunk splits a list into correct sized groups."""
    data = list(range(10))
    result = list(chunk(3, data))
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    # Ensure original data is unchanged
    assert data == list(range(10))

def test_chunk_boundary_empty_and_single():
    """Check behavior with empty iterable and single element."""
    # Empty iterable should yield nothing
    assert list(chunk(5, [])) == []

    # Single element should produce one chunk with that element
    assert list(chunk(5, [42])) == [[42]]

def test_chunk_error_invalid_n():
    """Chunk should raise ValueError when n <= 0."""
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(0, [1, 2, 3]))
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(-3, [1, 2, 3]))
