import pytest
import html
from tornado.escape import xhtml_unescape

def test_unescape_basic_string():
    # Basic HTML entities should be converted to their characters
    input_str = "Tom &amp; Jerry &lt;3 &quot;C++&quot;"
    expected = 'Tom & Jerry <3 "C++"'
    assert xhtml_unescape(input_str) == expected

def test_unescape_bytes_input():
    # Bytes input should be decoded and unescaped, always returning a str
    input_bytes = b"Hello &amp; World &#x1F600;"
    expected = "Hello & World 😀"
    result = xhtml_unescape(input_bytes)
    assert isinstance(result, str)
    assert result == expected

def test_unescape_invalid_surrogate_raises():
    # Surrogate pairs are invalid in HTML5 and should raise a ValueError
    # The surrogate pair U+D800 U+DC00 is represented in UTF-8 as b'\xed\xa0\x80\xed\x80\x80'
    invalid_bytes = b"\\uD800\\uDC00"
    with pytest.raises(ValueError):
        xhtml_unescape(invalid_bytes)
