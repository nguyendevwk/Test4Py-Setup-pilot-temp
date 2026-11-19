import pytest
import urllib.parse
from tornado.escape import url_unescape


def test_url_unescape_bytes_and_plus_handling():
    # Input is bytes, plus signs should be converted to spaces
    raw = b"Hello+World%21+%2B+%2B"
    result = url_unescape(raw, encoding="utf-8", plus=True)
    assert isinstance(result, str)
    assert result == "Hello World! + +"

    # When plus is False, plus signs remain literal
    result_no_plus = url_unescape(raw, encoding="utf-8", plus=False)
    assert result_no_plus == "Hello+World! + +"


def test_url_unescape_encoding_none_returns_bytes():
    # When encoding is None, result should be bytes and plus signs are replaced with spaces
    raw = b"foo+bar%20baz"
    result = url_unescape(raw, encoding=None, plus=True)
    assert isinstance(result, bytes)
    assert result == b"foo bar baz"

    # With plus=False, plus signs are preserved
    result_no_plus = url_unescape(raw, encoding=None, plus=False)
    assert result_no_plus == b"foo+bar baz"


def test_url_unescape_invalid_encoding_raises():
    # Using an unsupported encoding should raise a UnicodeDecodeError
    raw = "äöü".encode("utf-8")
    with pytest.raises(UnicodeDecodeError):
        url_unescape(raw, encoding="invalid-encoding", plus=True)
