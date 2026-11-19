import pytest
from tornado.escape import to_unicode

def test_to_unicode_returns_same_for_str_and_none():
    # Unicode string should be returned unchanged
    original = "hello world"
    assert to_unicode(original) is original
    # None should be returned unchanged
    assert to_unicode(None) is None

def test_to_unicode_decodes_bytes_and_handles_empty():
    # Bytes should be decoded to a unicode string
    b = b"foo\x00bar"
    decoded = to_unicode(b)
    assert isinstance(decoded, str)
    assert decoded == "foo\x00bar"
    # Empty bytes should decode to an empty string
    assert to_unicode(b"") == ""

def test_to_unicode_raises_on_invalid_type():
    # Passing an integer should raise a TypeError
    with pytest.raises(TypeError) as excinfo:
        to_unicode(42)
    assert "Expected bytes, unicode, or None" in str(excinfo.value)
