import pytest
from tornado.escape import url_unescape

def test_url_unescape_basic():
    # Basic percent-encoding and plus handling
    encoded = "Hello%20World%21+Testing%2B"
    # plus=True interprets '+' as space
    result = url_unescape(encoded, encoding="utf-8", plus=True)
    assert result == "Hello World! Testing+"
    # plus=False treats '+' literally
    result_plus_false = url_unescape(encoded, encoding="utf-8", plus=False)
    assert result_plus_false == "Hello World!+Testing+"

def test_url_unescape_bytes_and_none_encoding():
    # Input as bytes, encoding=None should return bytes
    encoded_bytes = b"foo%20bar%2Bbaz"
    result_bytes = url_unescape(encoded_bytes, encoding=None, plus=True)
    assert isinstance(result_bytes, bytes)
    assert result_bytes == b"foo bar baz"
    # plus=False with bytes input
    result_bytes_plus_false = url_unescape(encoded_bytes, encoding=None, plus=False)
    assert result_bytes_plus_false == b"foo bar+baz"

def test_url_unescape_invalid_input():
    # Passing an int should raise TypeError
    with pytest.raises(TypeError):
        url_unescape(123, encoding="utf-8", plus=True)
    # Passing a list should also raise TypeError
    with pytest.raises(TypeError):
        url_unescape(["not", "a", "string"], encoding="utf-8", plus=True)
