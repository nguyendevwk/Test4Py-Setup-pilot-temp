import pytest
from tornado.escape import linkify

def test_basic_linkify():
    """Normal URL should be converted to an <a> tag with http:// prefix."""
    input_text = "Check out https://example.com/page."
    expected = 'Check out <a href="https://example.com/page">https://example.com/page</a>.'
    assert linkify(input_text) == expected

def test_shorten_long_url():
    """Long URL should be shortened when shorten=True and title added."""
    long_url = "https://example.com/very/long/path/to/resource?query=param&another=thing"
    input_text = f"Visit {long_url} for details."
    result = linkify(input_text, shorten=True)
    # The displayed URL should be truncated and end with '...'
    assert '...' in result
    # The href should be the full original URL
    assert f'href="{long_url}"' in result
    # The title attribute should contain the full URL
    assert f'title="{long_url}"' in result

def test_require_protocol_and_invalid_protocol():
    """URLs without protocol should not be linkified when require_protocol=True."""
    input_text = "Visit www.example.com or http://safe.com."
    result = linkify(input_text, require_protocol=True)
    # www.example.com should remain plain text
    assert "www.example.com" in result and "<a" not in result.split("www.example.com")[1]
    # http://safe.com should be linkified
    assert '<a href="http://safe.com">http://safe.com</a>' in result
