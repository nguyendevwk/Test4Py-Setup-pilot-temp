import pytest
from tornado.escape import url_escape

def test_url_escape_default_plus():
    # Normal case: spaces become '+' and slashes become '%2F'
    result = url_escape("a b/c")
    assert result == "a+b%2Fc"

def test_url_escape_bytes_and_no_plus():
    # Boundary case: bytes input and plus=False keeps slashes
    data = b"foo bar/baz"
    result = url_escape(data, plus=False)
    # urllib.parse.quote on bytes returns a string with percent-encoding
    assert result == "foo%20bar/baz"

def test_url_escape_invalid_type():
    # Error case: passing an unsupported type should raise TypeError
    with pytest.raises(TypeError):
        url_escape(123)
