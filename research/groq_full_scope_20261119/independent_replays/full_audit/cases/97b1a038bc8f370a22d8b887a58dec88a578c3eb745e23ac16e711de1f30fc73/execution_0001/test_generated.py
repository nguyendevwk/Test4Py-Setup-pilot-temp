import pytest
from httpie.plugins.base import FormatterPlugin


def test_formatters_return_input_unmodified():
    """FormatterPlugin should return the same string for headers, body and metadata."""
    plugin = FormatterPlugin(format_options={})
    headers = "Content-Type: application/json\n"
    body = '{"key":"value"}'
    metadata = "Response time: 123ms"

    assert plugin.format_headers(headers) == headers
    assert plugin.format_body(body, "application/json") == body
    assert plugin.format_metadata(metadata) == metadata


def test_formatters_handle_empty_strings():
    """FormatterPlugin should handle empty strings without error."""
    plugin = FormatterPlugin(format_options={})
    assert plugin.format_headers("") == ""
    assert plugin.format_body("", "text/plain") == ""
    assert plugin.format_metadata("") == ""


def test_missing_format_options_raises_key_error():
    """Initializing FormatterPlugin without 'format_options' should raise KeyError."""
    with pytest.raises(KeyError):
        FormatterPlugin()
