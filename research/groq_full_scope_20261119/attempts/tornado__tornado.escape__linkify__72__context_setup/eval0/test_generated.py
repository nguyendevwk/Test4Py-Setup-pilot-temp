import pytest
from tornado.escape import linkify, _URL_RE, xhtml_escape, to_unicode


def test_linkify_basic_url():
    """Linkify a simple http URL and verify the output."""
    text = "Visit http://example.com for more info."
    result = linkify(text)
    # The URL should be wrapped in an <a> tag with the same href and text.
    assert '<a href="http://example.com">http://example.com</a>' in result
    # The surrounding text should remain unchanged.
    assert result.startswith("Visit ")
    assert result.endswith(" for more info.")


def test_linkify_shorten_long_url():
    """When shorten=True, long URLs are truncated and a title attribute is added."""
    long_url = "http://example.com/this/is/a/very/long/path/that/should/be/shortened"
    text = f"Check {long_url} now."
    result = linkify(text, shorten=True)
    # The link text should be shorter than the original URL.
    assert long_url not in result
    # The href should still contain the full URL.
    assert f'href="{long_url}"' in result
    # The title attribute should be present with the full URL.
    assert f'title="{long_url}"' in result
    # The link text should end with '...' indicating truncation.
    assert result.split('>')[1].endswith("...<") or result.split('>')[1].endswith("...<")  # noqa: E501


def test_linkify_bytes_input_and_protocol_requirement():
    """Linkify should accept bytes and respect require_protocol."""
    # Bytes input should be decoded to str internally.
    bytes_text = b"Visit www.example.com or http://example.com"
    result = linkify(bytes_text, require_protocol=True)
    # URLs without protocol should not be linkified when require_protocol=True.
    assert 'www.example.com' in result
    assert '<a href="http://www.example.com"' not in result
    # URLs with protocol should be linkified.
    assert '<a href="http://example.com">http://example.com</a>' in result
