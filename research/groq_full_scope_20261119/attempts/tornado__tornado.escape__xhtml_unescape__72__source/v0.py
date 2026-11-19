import pytest
import html
from tornado.escape import xhtml_unescape

def test_unescape_basic_string():
    # Normal HTML escape sequences should be converted to characters
    escaped = "Tom &amp; Jerry &lt;3 &quot;C++&quot; &#169;"
    expected = "Tom & Jerry <3 \"C++\" ©"
    assert xhtml_unescape(escaped) == expected

def test_unescape_bytes_input():
    # When given bytes, the function should return a str, not bytes
    escaped_bytes = b"&#x1F600; &#x1F602; &#x1F603;"
    expected = "😀 😂 😃"
    result = xhtml_unescape(escaped_bytes)
    assert isinstance(result, str)
    assert result == expected

def test_unescape_invalid_surrogate_raises():
    # Surrogate code points are invalid and should raise a ValueError
    # The string contains a high surrogate followed by a low surrogate
    invalid = "Invalid: \uD800\uDC00"
    with pytest.raises(ValueError):
        xhtml_unescape(invalid)
