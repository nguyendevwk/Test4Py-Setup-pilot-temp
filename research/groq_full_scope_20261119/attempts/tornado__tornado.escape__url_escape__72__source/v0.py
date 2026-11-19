import pytest
from tornado.escape import url_escape

def test_url_escape_plus_true():
    # Spaces become '+' and slashes become '%2F'
    assert url_escape("a b/c") == "a+b%2Fc"
    # Characters that need encoding are percent-encoded
    assert url_escape("äöü") == "%C3%A4%C3%B6%C3%BC"

def test_url_escape_plus_false():
    # Spaces become '%20' and slashes remain unchanged
    assert url_escape("a b/c", plus=False) == "a%20b/c"
    # Verify that plus signs are encoded when plus=False
    assert url_escape("a+b", plus=False) == "a%2Bb"

def test_url_escape_invalid_type():
    # Passing bytes should raise a TypeError because urllib.parse.quote expects a string
    with pytest.raises(TypeError):
        url_escape(b"bytes")
