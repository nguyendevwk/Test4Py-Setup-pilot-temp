import pytest
import urllib.parse
from tornado.escape import url_unescape

def test_url_unescape_bytes_and_plus_handling():
    # Input bytes with percent-encoding and plus signs
    raw = b"Hello%20World%21+Testing%2Bplus"
    # Default plus=True: plus becomes space
    result = url_unescape(raw, encoding="utf-8", plus=True)
    assert isinstance(result, str)
    assert result == "Hello World! Testing+plus"

    # plus=False: plus remains literal
    result_no_plus = url_unescape(raw, encoding="utf-8", plus=False)
    assert result_no_plus == "Hello World! Testing+plus"

def test_url_unescape_encoding_none_returns_bytes():
    # When encoding is None, result should be bytes
    raw = b"%41%42%43+%44"
    result = url_unescape(raw, encoding=None, plus=True)
    assert isinstance(result, bytes)
    # plus sign replaced with space before unquoting
    assert result == b"ABC D"

    # plus=False should not replace plus
    result_no_plus = url_unescape(raw, encoding=None, plus=False)
    assert result_no_plus == b"ABC+ D"

def test_url_unescape_invalid_percent_sequences():
    # Percent sequences that are not valid hex should be left unchanged
    raw = "Invalid%G1%ZZ%20Text"
    result = url_unescape(raw, encoding="utf-8", plus=True)
    # Only the valid %20 is decoded to space
    assert result == "Invalid%G1%ZZ Text"

    # With encoding=None, the raw bytes are returned unchanged except for plus
    raw_bytes = b"Invalid%G1%ZZ%20Text+"
    result_bytes = url_unescape(raw_bytes, encoding=None, plus=True)
    assert result_bytes == b"Invalid%G1%ZZ Text "
