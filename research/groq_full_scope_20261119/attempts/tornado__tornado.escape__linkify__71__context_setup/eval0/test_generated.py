import pytest
from tornado.escape import linkify

def test_basic_linkify():
    """Linkify a simple URL with protocol."""
    text = "Visit http://example.com for more info."
    result = linkify(text)
    expected = 'Visit <a href="http://example.com">http://example.com</a> for more info.'
    assert result == expected

def test_shorten_long_url():
    """When shorten=True, long URLs are truncated and title added."""
    long_url = "http://example.com/very/long/path/with/many/segments?query=param&another=val"
    text = f"Check this out: {long_url}"
    result = linkify(text, shorten=True)
    # The link text should be shortened but still contain the host and first path part
    assert '<a href="http://example.com/very/long/path/with/many/segments?query=param&another=val"' in result
    # The displayed text should be truncated and end with '...'
    assert result.split('>')[1].startswith("http://example.com/very/long/path/with/many/seg")
    assert result.split('>')[1].endswith("...")

def test_require_protocol_and_permitted_protocols():
    """URLs without protocol are not linkified when require_protocol=True."""
    text = "Visit www.example.com or http://example.com"
    result = linkify(text, require_protocol=True)
    # www.example.com should remain plain text
    assert "www.example.com" in result and "<a href" not in result.split("www.example.com")[1]
    # http://example.com should be linkified
    assert '<a href="http://example.com">http://example.com</a>' in result
