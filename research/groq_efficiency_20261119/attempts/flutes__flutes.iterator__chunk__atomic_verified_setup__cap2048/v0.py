import pytest
from flutes.iterator import chunk

def test_chunk_basic_split():
    """Normal case: split a range into chunks of size 3."""
    result = list(chunk(3, range(10)))
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    # Ensure that the last chunk is smaller when the total is not a multiple of n
    assert len(result[-1]) == 1
    assert result[-1] == [9]

def test_chunk_boundary_empty_and_small():
    """Boundary cases: empty iterable and chunk size larger than iterable."""
    # Empty iterable should yield nothing
    assert list(chunk(5, [])) == []
    # Chunk size larger than iterable should return the whole iterable as one chunk
    data = [1, 2]
    assert list(chunk(10, data)) == [data]

def test_chunk_invalid_n_raises():
    """Error case: non‑positive chunk size raises ValueError."""
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(0, [1, 2, 3]))
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(-3, [1, 2, 3]))
