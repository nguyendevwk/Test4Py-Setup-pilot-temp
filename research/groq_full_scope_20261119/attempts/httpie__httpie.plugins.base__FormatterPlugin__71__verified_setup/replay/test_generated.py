import pytest
from httpie.plugins.base import FormatterPlugin


def test_initialization_sets_attributes():
    """FormatterPlugin should store provided kwargs and expose them."""
    plugin = FormatterPlugin(format_options={'opt': True}, other='value')
    assert plugin.enabled is True
    assert plugin.kwargs == {'format_options': {'opt': True}, 'other': 'value'}
    assert plugin.format_options == {'opt': True}


def test_format_headers_returns_input():
    """format_headers should return the headers string unchanged."""
    plugin = FormatterPlugin(format_options={})
    headers = "Content-Type: application/json\nX-Test: 123"
    result = plugin.format_headers(headers)
    assert result is headers  # identity check
    assert result == headers  # content check


def test_format_body_returns_input():
    """format_body should return the content string unchanged regardless of mime."""
    plugin = FormatterPlugin(format_options={})
    content = "<html><body>Hello</body></html>"
    mime = "text/html"
    result = plugin.format_body(content, mime)
    assert result is content
    assert result == content
