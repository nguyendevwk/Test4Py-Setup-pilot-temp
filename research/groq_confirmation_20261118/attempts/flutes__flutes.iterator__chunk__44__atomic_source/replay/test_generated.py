import pytest
from flutes.iterator import chunk

def test_chunk_normal_behavior():
    """Verify that chunk splits a range into correct sized sublists."""
    result = list(chunk(3, range(10)))
    expected = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    assert result == expected, f"Expected {expected}, got {result}"

def test_chunk_boundary_cases():
    """Test edge cases: n equals 1 and n larger than iterable length."""
    # n == 1 should return each element in its own list
    single = list(chunk(1, [10, 20, 30]))
    assert single == [[10], [20], [30]], f"Expected each element in its own list, got {single}"
    # n larger than iterable length should return the whole iterable as one chunk
    large_n = list(chunk(100, [1, 2, 3]))
    assert large_n == [[1, 2, 3]], f"Expected entire iterable as one chunk, got {large_n}"

def test_chunk_invalid_n_raises_value_error():
    """Ensure that providing a non‑positive n raises ValueError."""
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(0, [1, 2, 3]))
    with pytest.raises(ValueError, match="`n` should be positive"):
        list(chunk(-5, [1, 2, 3]))
