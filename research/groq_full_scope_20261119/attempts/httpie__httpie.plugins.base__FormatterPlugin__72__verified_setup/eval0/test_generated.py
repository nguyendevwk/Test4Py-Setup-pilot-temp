import pytest
from httpie.plugins.base import FormatterPlugin

def test_initialization_sets_attributes():
    plugin = FormatterPlugin(format_options={'opt': True}, other='value')
    assert plugin.enabled is True
    assert plugin.kwargs == {'format_options': {'opt': True}, 'other': 'value'}
    assert plugin.format_options == {'opt': True}

def test_format_headers_returns_input():
    plugin = FormatterPlugin(format_options={})
    headers = "Content-Type: application/json\nX-Test: 123"
    result = plugin.format_headers(headers)
    assert result is headers  # identity, not a copy
    assert isinstance(result, str)

def test_format_body_and_metadata_identity():
    plugin = FormatterPlugin(format_options={})
    body = "<html><body>Hello</body></html>"
    mime = "text/html"
    body_result = plugin.format_body(body, mime)
    assert body_result is body
    metadata = "Response time: 200ms"
    meta_result = plugin.format_metadata(metadata)
    assert meta_result is metadata
