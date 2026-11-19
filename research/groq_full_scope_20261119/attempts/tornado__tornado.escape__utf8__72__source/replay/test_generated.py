import pytest
from tornado.escape import utf8
from tornado.util import unicode_type

def test_utf8_converts_unicode_to_bytes():
    # Normal unicode string should be encoded to UTF‑8 bytes
    s = "café"
    result = utf8(s)
    assert isinstance(result, bytes)
    assert result == s.encode("utf-8")

def test_utf8_returns_bytes_and_none_unmodified():
    # Bytes and None should be returned unchanged
    b = b"hello"
    n = None
    assert utf8(b) is b
    assert utf8(n) is None

def test_utf8_raises_type_error_for_invalid_input():
    # Passing an int should raise a TypeError
    with pytest.raises(TypeError) as excinfo:
        utf8(42)
    assert "Expected bytes, unicode, or None" in str(excinfo.value)
