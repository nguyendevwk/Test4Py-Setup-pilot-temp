import pytest
from tornado.escape import to_unicode

def test_to_unicode_returns_same_for_str_and_none():
    # Passing a unicode string should return the same object unchanged
    original = "hello world"
    result = to_unicode(original)
    assert result is original
    # Passing None should return None unchanged
    assert to_unicode(None) is None

def test_to_unicode_decodes_bytes_and_handles_empty():
    # Bytes should be decoded to a unicode string
    byte_input = b"foo\x00bar"
    decoded = to_unicode(byte_input)
    assert isinstance(decoded, str)
    assert decoded == "foo\x00bar"
    # Empty bytes should decode to an empty string
    assert to_unicode(b"") == ""

def test_to_unicode_raises_type_error_for_invalid_input():
    # Passing an integer should raise a TypeError
    with pytest.raises(TypeError) as excinfo:
        to_unicode(123)
    assert "Expected bytes, unicode, or None" in str(excinfo.value)
