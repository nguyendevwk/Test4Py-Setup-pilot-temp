import pytest
import urllib.parse
from tornado.escape import url_unescape


def test_url_unescape_basic_string_and_bytes():
    # Normal string with percent-encoding and plus signs
    encoded = "Hello%20World%21+Test%2B"
    # Default plus=True: plus becomes space
    result = url_unescape(encoded)
    assert result == "Hello World! Test+"

    # Bytes input should be handled similarly
    encoded_bytes = b"Foo%2BBar%20%26%20Baz"
    result_bytes = url_unescape(encoded_bytes)
    assert result_bytes == "Foo+Bar & Baz"

    # Verify that the result is a str when encoding is not None
    assert isinstance(result, str)
    assert isinstance(result_bytes, str)


def test_url_unescape_encoding_none_and_plus_flag():
    # When encoding is None, result should be bytes
    encoded = "A%20B%2B"
    # plus=True: replace '+' with space before unquoting
    result = url_unescape(encoded, encoding=None, plus=True)
    assert isinstance(result, bytes)
    assert result == urllib.parse.unquote_to_bytes(encoded.replace("+", " "))

    # plus=False: do not replace '+' before unquoting
    result_no_plus = url_unescape(encoded, encoding=None, plus=False)
    assert isinstance(result_no_plus, bytes)
    assert result_no_plus == urllib.parse.unquote_to_bytes(encoded)


def test_url_unescape_invalid_input_type():
    # Passing an unsupported type should raise a TypeError
    with pytest.raises(TypeError):
        url_unescape(12345)  # int is not a valid input type
