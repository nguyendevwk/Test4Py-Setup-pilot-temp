import pytest
from tornado.escape import utf8

def test_utf8_encodes_unicode_string_to_bytes():
    # A normal Unicode string should be encoded to UTF‑8 bytes
    original = "café"
    result = utf8(original)
    assert isinstance(result, bytes)
    assert result == b"caf\xc3\xa9"

def test_utf8_returns_bytes_and_none_unmodified():
    # Bytes and None should be returned unchanged
    byte_input = b"hello"
    none_input = None
    assert utf8(byte_input) is byte_input
    assert utf8(none_input) is none_input

def test_utf8_raises_type_error_for_invalid_type():
    # Passing an integer should raise a TypeError
    with pytest.raises(TypeError) as excinfo:
        utf8(42)
    assert "Expected bytes, unicode, or None" in str(excinfo.value)
