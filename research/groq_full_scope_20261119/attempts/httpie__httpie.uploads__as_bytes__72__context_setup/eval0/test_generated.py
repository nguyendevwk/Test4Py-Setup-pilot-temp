import pytest
from httpie.uploads import as_bytes

def test_as_bytes_with_string_returns_encoded_bytes():
    """Normal case: a string should be encoded to bytes."""
    input_str = "hello world"
    result = as_bytes(input_str)
    assert isinstance(result, bytes)
    assert result == b"hello world"
    # Ensure the original string is unchanged
    assert input_str == "hello world"

def test_as_bytes_with_bytes_returns_same_object():
    """Boundary case: passing bytes should return the same object unchanged."""
    input_bytes = b"binary data"
    result = as_bytes(input_bytes)
    assert isinstance(result, bytes)
    assert result is input_bytes  # same object
    assert result == b"binary data"

def test_as_bytes_with_non_string_non_bytes_returns_unmodified():
    """Error-like scenario: passing an unsupported type returns it unchanged."""
    input_int = 42
    result = as_bytes(input_int)
    # The function does not raise; it simply returns the input
    assert result is input_int
    assert isinstance(result, int)
