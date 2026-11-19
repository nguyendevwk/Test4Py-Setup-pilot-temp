import pytest
from flutes.iterator import chunk

def test_chunk_basic():
    """Normal case: split a range into chunks of size 3."""
    result = list(chunk(3, range(10)))
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    # Ensure each chunk is a list and has at most 3 elements
    for sub in result:
        assert isinstance(sub, list)
        assert len(sub) <= 3

def test_chunk_boundary_empty_and_single():
    """Boundary case: empty iterable and chunk size larger than iterable."""
    # Empty iterable
    assert list(chunk(5, [])) == []
    # Chunk size larger than iterable
    assert list(chunk(10, [1, 2, 3])) == [[1, 2, 3]]

def test_chunk_error_invalid_n():
    """Error case: non‑positive chunk size raises ValueError."""
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(0, [1, 2, 3]))
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(-1, [1, 2, 3]))
