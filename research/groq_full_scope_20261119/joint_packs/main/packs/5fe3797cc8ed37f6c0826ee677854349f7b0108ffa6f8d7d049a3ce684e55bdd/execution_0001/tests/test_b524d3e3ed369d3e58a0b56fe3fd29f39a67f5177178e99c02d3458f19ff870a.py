import pytest
import urllib.parse
from tornado.escape import url_unescape

def test_url_unescape_basic():
    # Normal decoding of percent-encoded string with plus as space
    encoded = "Hello+World%21+%26+%3D"
    result = url_unescape(encoded)
    assert result == "Hello World! & ="

    # Decoding with plus disabled should keep plus signs
    result_plus_disabled = url_unescape(encoded, plus=False)
    assert result_plus_disabled == "Hello+World!+&+="

def test_url_unescape_bytes_and_encoding_none():
    # When encoding is None, result should be bytes and plus signs replaced by spaces
    encoded_bytes = b"foo+bar%20baz"
    result_bytes = url_unescape(encoded_bytes, encoding=None)
    assert isinstance(result_bytes, bytes)
    assert result_bytes == b"foo bar baz"

    # If plus is False, plus signs should remain unchanged
    result_bytes_plus_false = url_unescape(encoded_bytes, encoding=None, plus=False)
    assert result_bytes_plus_false == urllib.parse.unquote_to_bytes(encoded_bytes)

def test_url_unescape_invalid_input():
    # Passing an integer should raise TypeError
    with pytest.raises(TypeError):
        url_unescape(123)
