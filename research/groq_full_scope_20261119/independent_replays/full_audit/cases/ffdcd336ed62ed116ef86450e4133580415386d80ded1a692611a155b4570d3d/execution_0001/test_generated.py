import pytest
from tornado.escape import utf8
from tornado.util import unicode_type

def test_utf8_encodes_unicode_string_to_bytes():
    # Normal case: a Unicode string should be encoded to UTF‑8 bytes
    text = "café"  # contains a non‑ASCII character
    result = utf8(text)
    assert isinstance(result, bytes)
    assert result == b"caf\xc3\xa9"

def test_utf8_returns_bytes_and_none_unmodified():
    # Bytes and None should be returned unchanged
    b = b"hello"
    n = None
    assert utf8(b) is b
    assert utf8(n) is None

def test_utf8_raises_type_error_on_invalid_type():
    # Passing an integer should raise a TypeError
    with pytest.raises(TypeError) as excinfo:
        utf8(123)
    assert "Expected bytes, unicode, or None" in str(excinfo.value)
