import pytest
from tornado.escape import url_escape

def test_url_escape_default_plus_behavior():
    # Normal string with spaces and slashes
    s = "a b/c"
    escaped = url_escape(s)  # default plus=True
    assert escaped == "a+b%2Fc", "Default plus=True should encode spaces as + and slashes as %2F"

def test_url_escape_no_plus_behavior_and_bytes():
    # When plus=False, spaces become %20 and slashes remain
    s = "a b/c"
    escaped = url_escape(s, plus=False)
    assert escaped == "a%20b/c", "plus=False should encode spaces as %20 and leave slashes"

    # Bytes input should be handled correctly
    b = b"foo bar"
    escaped_bytes = url_escape(b, plus=True)
    assert escaped_bytes == "foo+bar", "Bytes input should be encoded like str with plus=True"

def test_url_escape_invalid_type_raises():
    # Passing an unsupported type should raise TypeError
    with pytest.raises(TypeError):
        url_escape(123)  # int is not a valid type for url_escape
