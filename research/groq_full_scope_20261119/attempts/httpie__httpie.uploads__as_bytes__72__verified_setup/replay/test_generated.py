import pytest
from httpie.uploads import as_bytes

def test_as_bytes_with_string_encodes_to_bytes():
    """String input should be encoded to bytes using UTF-8."""
    input_str = "hello world"
    result = as_bytes(input_str)
    assert isinstance(result, bytes)
    assert result == b"hello world"

def test_as_bytes_with_bytes_returns_same_object():
    """Bytes input should be returned unchanged."""
    input_bytes = b"\x00\x01\x02"
    result = as_bytes(input_bytes)
    assert result is input_bytes  # same object, not a copy

def test_as_bytes_with_non_string_non_bytes_returns_input():
    """Non-string/non-bytes input should be returned unchanged."""
    input_int = 42
    result = as_bytes(input_int)
    assert result is input_int
