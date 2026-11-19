import pytest
from tornado.escape import utf8, _UTF8_TYPES
from tornado.util import unicode_type

def test_utf8_accepts_bytes_and_none():
    # Bytes should be returned unchanged
    data = b"hello"
    assert utf8(data) is data
    # None should be returned unchanged
    assert utf8(None) is None

def test_utf8_encodes_unicode_strings():
    # Unicode string should be encoded to UTF-8 bytes
    text = "café"
    encoded = utf8(text)
    assert isinstance(encoded, bytes)
    assert encoded == text.encode("utf-8")
    # Ensure that the original string is not modified
    assert text == "café"

def test_utf8_rejects_invalid_types():
    # Passing an integer should raise a TypeError
    with pytest.raises(TypeError) as excinfo:
        utf8(42)
    assert "Expected bytes, unicode, or None" in str(excinfo.value)
    # Passing a list should also raise a TypeError
    with pytest.raises(TypeError):
        utf8([1, 2, 3])
