import pytest
from tornado.escape import to_unicode

def test_to_unicode_returns_unmodified_string():
    original = "hello world"
    result = to_unicode(original)
    assert result is original
    assert isinstance(result, str)

def test_to_unicode_decodes_bytes_and_handles_empty():
    data = b"foo\x00bar"
    result = to_unicode(data)
    assert result == "foo\x00bar"
    assert isinstance(result, str)
    empty = b""
    assert to_unicode(empty) == ""

def test_to_unicode_raises_on_invalid_type():
    with pytest.raises(TypeError) as excinfo:
        to_unicode(123)
    assert "Expected bytes, unicode, or None" in str(excinfo.value)
