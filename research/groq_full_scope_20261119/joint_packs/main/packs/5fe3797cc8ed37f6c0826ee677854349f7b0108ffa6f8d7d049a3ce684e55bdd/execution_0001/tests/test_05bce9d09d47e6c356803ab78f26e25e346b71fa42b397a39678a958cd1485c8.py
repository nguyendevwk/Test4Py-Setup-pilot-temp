import pytest
import html
from tornado.escape import xhtml_unescape

def test_unescape_basic_string():
    # Normal HTML escape sequences should be converted to characters
    escaped = "Tom &amp; Jerry &lt;3 &quot;C++&quot;"
    expected = "Tom & Jerry <3 \"C++\""
    assert xhtml_unescape(escaped) == expected

def test_unescape_bytes_input():
    # Bytes input should be decoded and unescaped, returning a str
    escaped_bytes = b"&#x1F600; &#x1F602;"  # 😀 😂
    expected = "😀 😂"
    result = xhtml_unescape(escaped_bytes)
    assert isinstance(result, str)
    assert result == expected

def test_unescape_invalid_surrogate_raises():
    # Surrogate pairs are invalid in HTML5 and should raise a ValueError
    # The surrogate pair U+D800 U+DC00 is represented in UTF-8 as b'\xed\xa0\x80\xed\xb0\x80'
    invalid_bytes = b"\xed\xa0\x80\xed\xb0\x80"
    with pytest.raises(ValueError):
        xhtml_unescape(invalid_bytes)
