import pytest
from flutes.iterator import chunk

def test_chunk_basic_split():
    """Normal case: split a range into chunks of size 3."""
    result = list(chunk(3, range(10)))
    assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    # Ensure that each chunk is a list and not a reference to the same list
    assert all(isinstance(chunk, list) for chunk in result)
    assert len(result) == 4
    assert result[0] is not result[1]  # distinct objects

def test_chunk_boundary_small_and_large():
    """Boundary cases: n larger than iterable and n equal to 1."""
    # n larger than iterable
    large_n = 20
    data = [1, 2, 3]
    result_large = list(chunk(large_n, data))
    assert result_large == [data]
    # n equal to 1
    result_single = list(chunk(1, data))
    assert result_single == [[1], [2], [3]]
    # Ensure no empty chunks are produced
    assert all(chunk for chunk in result_single)

def test_chunk_invalid_n_raises():
    """Error case: n must be positive."""
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(0, [1, 2, 3]))
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(-5, [1, 2, 3]))
