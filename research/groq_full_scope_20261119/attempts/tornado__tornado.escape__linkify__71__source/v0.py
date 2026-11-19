import pytest
from tornado.escape import linkify

def test_basic_linkify():
    """Normal URL with protocol should be converted to an <a> tag."""
    input_text = "Visit http://example.com for more info."
    result = linkify(input_text)
    expected = 'Visit <a href="http://example.com">http://example.com</a> for more info.'
    assert result == expected

def test_shorten_long_url():
    """Long URLs should be shortened when shorten=True."""
    long_url = "http://example.com/this/is/a/very/long/path/with/many/segments?query=param&another=param2"
    input_text = f"Check this out: {long_url}"
    result = linkify(input_text, shorten=True)
    # The displayed URL should be truncated and end with '...'
    assert '<a href="http://example.com/this/is/a/very/long/path/with/many/segments?query=param&another=param2"' in result
    assert result.count('...') == 1
    # The title attribute should contain the full URL
    assert f'title="{long_url}"' in result

def test_require_protocol_and_permitted():
    """URLs without protocol should not be linkified when require_protocol=True."""
    input_text = "Visit www.example.com or http://allowed.com"
    result = linkify(input_text, require_protocol=True, permitted_protocols=["http"])
    # www.example.com should remain plain text
    assert "www.example.com" in result
    # http://allowed.com should be linkified
    assert '<a href="http://allowed.com">http://allowed.com</a>' in result
