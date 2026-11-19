import pytest
from tornado.escape import to_unicode

def test_to_unicode_returns_same_for_str_and_none():
    # Normal case: unicode string should be returned unchanged
    s = "hello world"
    assert to_unicode(s) is s
    # None should also be returned unchanged
    assert to_unicode(None) is None

def test_to_unicode_decodes_bytes_and_handles_boundary():
    # Boundary case: empty bytes should decode to empty string
    assert to_unicode(b"") == ""
    # Typical bytes decoding
    b = b"\xc3\xa9"  # 'é' in UTF-8
    assert to_unicode(b) == "é"

def test_to_unicode_raises_type_error_for_invalid_input():
    # Error case: passing an int should raise TypeError
    with pytest.raises(TypeError, match="Expected bytes, unicode, or None"):
        to_unicode(42)
