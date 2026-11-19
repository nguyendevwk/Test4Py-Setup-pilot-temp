import pytest
from flutes.iterator import chunk

def test_chunk_basic():
    """Normal case: split a range into chunks of size 3."""
    result = list(chunk(3, range(10)))
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    # Ensure that each chunk is a list and not a reference to the same list
    assert all(isinstance(chunk, list) for chunk in result)
    assert len(result) == 4
    assert result[0] is not result[1]

def test_chunk_boundary():
    """Boundary case: chunk size equal to iterable length."""
    data = [1, 2, 3]
    result = list(chunk(3, data))
    assert result == [data]
    # The returned chunk should be a new list, not the original
    assert result[0] is not data
    assert result[0] == data

def test_chunk_invalid_n():
    """Error case: non‑positive chunk size raises ValueError."""
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(0, [1, 2, 3]))
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(-5, [1, 2, 3]))
