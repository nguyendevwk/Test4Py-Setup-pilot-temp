import pytest
from httpie.uploads import as_bytes

def test_as_bytes_with_string():
    """as_bytes should encode a string to UTF‑8 bytes."""
    original = "hello world"
    result = as_bytes(original)
    assert isinstance(result, bytes)
    assert result == b"hello world"
    # Ensure that the original string is unchanged
    assert original == "hello world"

def test_as_bytes_with_bytes():
    """as_bytes should return the same bytes object unchanged."""
    original = b"\x00\x01\x02"
    result = as_bytes(original)
    assert isinstance(result, bytes)
    assert result is original  # identity check
    assert result == b"\x00\x01\x02"

def test_as_bytes_with_empty_and_unicode():
    """as_bytes should handle empty strings and Unicode correctly."""
    empty = ""
    empty_result = as_bytes(empty)
    assert empty_result == b""

    unicode_str = "ñáéíóú"
    unicode_result = as_bytes(unicode_str)
    assert isinstance(unicode_result, bytes)
    assert unicode_result == unicode_str.encode()
