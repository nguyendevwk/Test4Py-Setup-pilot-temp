import pytest
from flutes.iterator import chunk

def test_chunk_basic():
    """Verify that chunk splits a range into correct sized groups."""
    result = list(chunk(3, range(10)))
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    # Ensure that the last chunk is smaller when not divisible
    assert len(result[-1]) == 1

def test_chunk_single_element():
    """When n is 1, each element should be its own chunk."""
    data = ['a', 'b', 'c']
    result = list(chunk(1, data))
    assert result == [['a'], ['b'], ['c']]
    # The number of chunks should equal the number of elements
    assert len(result) == len(data)

def test_chunk_invalid_n():
    """Providing a non‑positive n should raise ValueError."""
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(0, [1, 2, 3]))
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(-5, [1, 2, 3]))
