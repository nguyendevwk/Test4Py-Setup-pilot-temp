import pytest
from httpie.plugins.base import FormatterPlugin


def test_initialization_sets_attributes():
    plugin = FormatterPlugin(format_options={"opt": "value"}, other="data")
    assert plugin.enabled is True
    assert plugin.kwargs == {"format_options": {"opt": "value"}, "other": "data"}
    assert plugin.format_options == {"opt": "value"}


def test_format_headers_returns_input():
    plugin = FormatterPlugin(format_options={})
    headers = "Content-Type: application/json\nX-Custom: 123"
    result = plugin.format_headers(headers)
    assert result is headers  # identity check
    assert result == headers  # content equality


def test_format_body_and_metadata_return_input():
    plugin = FormatterPlugin(format_options={})
    body = "<html><body>Hello</body></html>"
    mime = "text/html"
    body_result = plugin.format_body(body, mime)
    assert body_result is body
    assert body_result == body

    metadata = "Response time: 200ms"
    meta_result = plugin.format_metadata(metadata)
    assert meta_result is metadata
    assert meta_result == metadata
