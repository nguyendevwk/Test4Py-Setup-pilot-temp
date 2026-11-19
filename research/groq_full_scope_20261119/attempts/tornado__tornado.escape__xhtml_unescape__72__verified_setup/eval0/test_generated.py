import pytest
import html
from tornado.escape import xhtml_unescape


def test_unescape_basic_string():
    """xhtml_unescape should correctly unescape a normal HTML-escaped string."""
    escaped = "Tom &amp; Jerry &lt;3 &#x1F600;"
    expected = "Tom & Jerry <3 😀"
    assert xhtml_unescape(escaped) == expected
    # Ensure the result is a str, not bytes
    assert isinstance(xhtml_unescape(escaped), str)


def test_unescape_bytes_input():
    """xhtml_unescape should accept bytes and always return a str."""
    escaped_bytes = b"Hello &amp; World &#x263A;"
    expected = "Hello & World ☺"
    result = xhtml_unescape(escaped_bytes)
    assert result == expected
    assert isinstance(result, str)


def test_unescape_invalid_surrogate_raises():
    """xhtml_unescape should raise ValueError for invalid surrogate references."""
    # The surrogate pair U+D800 is not a valid character on its own
    invalid = "&#xD800;"
    with pytest.raises(ValueError):
        xhtml_unescape(invalid)
