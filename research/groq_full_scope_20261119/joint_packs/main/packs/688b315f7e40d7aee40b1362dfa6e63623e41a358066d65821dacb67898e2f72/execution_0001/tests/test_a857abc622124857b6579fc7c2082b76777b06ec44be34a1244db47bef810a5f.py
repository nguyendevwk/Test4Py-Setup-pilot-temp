import pytest
from httpie.uploads import as_bytes

def test_as_bytes_with_string():
    """String input should be encoded to bytes."""
    original = "hello world"
    result = as_bytes(original)
    assert isinstance(result, bytes)
    assert result == b"hello world"
    # Ensure the result is a new object, not the original string
    assert result is not original

def test_as_bytes_with_bytes():
    """Bytes input should be returned unchanged."""
    original = b"binary data"
    result = as_bytes(original)
    assert isinstance(result, bytes)
    assert result == original
    # The returned object should be the same instance
    assert result is original

def test_as_bytes_with_empty_string():
    """Empty string should return an empty bytes object."""
    original = ""
    result = as_bytes(original)
    assert isinstance(result, bytes)
    assert result == b""
    assert result is not original
