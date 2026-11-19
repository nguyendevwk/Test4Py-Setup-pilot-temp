import pytest
import html
from tornado.escape import xhtml_unescape

def test_xhtml_unescape_basic_string():
    # Basic HTML escape sequences should be converted to their literal characters
    escaped = "Tom &amp; Jerry &lt;3 &quot;C++&quot; &#169;"
    expected = "Tom & Jerry <3 \"C++\" ©"
    assert xhtml_unescape(escaped) == expected

def test_xhtml_unescape_bytes_input():
    # When given bytes, the function should return a str, not bytes
    escaped_bytes = b"Hello &amp; world &#x1F600;"
    result = xhtml_unescape(escaped_bytes)
    assert isinstance(result, str)
    assert result == "Hello & world 😀"

def test_xhtml_unescape_invalid_surrogate_raises():
    # Surrogate code points are invalid and should raise ValueError
    invalid = "Invalid &#xD800; surrogate"
    with pytest.raises(ValueError):
        xhtml_unescape(invalid)
