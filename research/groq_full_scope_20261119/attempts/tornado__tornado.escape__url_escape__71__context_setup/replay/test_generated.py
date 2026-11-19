import pytest
from tornado.escape import url_escape

def test_url_escape_plus_true():
    # Normal string with spaces and slashes
    s = "a b/c"
    escaped = url_escape(s, plus=True)
    # Spaces become '+', slashes become '%2F'
    assert escaped == "a+b%2Fc"

def test_url_escape_plus_false():
    # Path component: spaces become '%20', slashes stay
    s = "a b/c"
    escaped = url_escape(s, plus=False)
    assert escaped == "a%20b/c"

def test_url_escape_invalid_type():
    # Passing an unsupported type should raise a TypeError
    with pytest.raises(TypeError):
        url_escape(123)  # int is not str or bytes
