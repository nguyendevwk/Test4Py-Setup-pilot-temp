import pytest
from flutes.iterator import chunk

def test_chunk_normal():
    """Normal case: split a list into chunks of size 3."""
    data = list(range(10))
    result = list(chunk(3, data))
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    # Ensure original data is unchanged
    assert data == list(range(10))

def test_chunk_boundary():
    """Boundary case: chunk size equal to iterable length."""
    data = [1, 2, 3]
    result = list(chunk(3, data))
    assert result == [[1, 2, 3]]
    # Chunk size larger than iterable
    result_larger = list(chunk(5, data))
    assert result_larger == [[1, 2, 3]]

def test_chunk_error():
    """Error case: non‑positive chunk size raises ValueError."""
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(0, [1, 2, 3]))
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(-1, [1, 2, 3]))
