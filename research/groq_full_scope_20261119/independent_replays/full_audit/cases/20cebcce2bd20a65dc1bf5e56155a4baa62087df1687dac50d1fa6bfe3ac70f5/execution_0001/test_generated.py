import pytest
from tornado.escape import url_escape

def test_url_escape_default_plus_behavior():
    # Normal string with spaces and slashes
    s = "a b/c"
    escaped = url_escape(s)  # default plus=True
    assert escaped == "a+b%2Fc", "Default plus=True should encode space as '+' and slash as '%2F'"

def test_url_escape_no_plus_behavior_and_bytes():
    # Explicitly disable plus encoding and test bytes input
    b = b"foo bar/baz"
    escaped = url_escape(b, plus=False)
    # Spaces should be '%20', slashes should remain '/'
    assert escaped == "foo%20bar/baz", "plus=False should encode space as '%20' and leave slashes"

def test_url_escape_invalid_type_raises():
    # Passing an unsupported type should raise a TypeError
    with pytest.raises(TypeError):
        url_escape(123)  # int is not a valid type for url_escape
