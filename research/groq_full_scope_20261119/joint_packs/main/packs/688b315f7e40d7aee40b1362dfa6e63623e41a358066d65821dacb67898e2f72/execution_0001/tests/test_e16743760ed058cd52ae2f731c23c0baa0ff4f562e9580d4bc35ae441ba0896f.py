import pytest
from httpie.uploads import as_bytes

def test_as_bytes_with_string():
    """String input should be encoded to bytes using default UTF-8."""
    original = "hello world"
    result = as_bytes(original)
    assert isinstance(result, bytes)
    assert result == b"hello world"
    # Ensure that the original string is unchanged
    assert original == "hello world"

def test_as_bytes_with_bytes():
    """Bytes input should be returned unchanged."""
    original = b"\x00\x01\x02"
    result = as_bytes(original)
    assert isinstance(result, bytes)
    assert result is original  # same object
    assert result == b"\x00\x01\x02"

def test_as_bytes_with_empty_values():
    """Empty string and empty bytes should be handled correctly."""
    empty_str = ""
    empty_bytes = b""
    assert as_bytes(empty_str) == b""
    assert as_bytes(empty_bytes) == b""
