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
    # Percent sequences that are incomplete or invalid should be left unchanged
    raw = "Incomplete%2"          # missing one hex digit
    result = url_unescape(raw, encoding="utf-8", plus=False)
    assert result == "Incomplete%2"

    raw_invalid = "%ZZ"           # non-hex digits
    result_invalid = url_unescape(raw_invalid, encoding="utf-8", plus=False)
    assert result_invalid == "%ZZ"

    # Bytes input with invalid percent
    raw_bytes = b"%G1%2"
    result_bytes = url_unescape(raw_bytes, encoding="utf-8", plus=False)
    assert result_bytes == "%G1%2"
