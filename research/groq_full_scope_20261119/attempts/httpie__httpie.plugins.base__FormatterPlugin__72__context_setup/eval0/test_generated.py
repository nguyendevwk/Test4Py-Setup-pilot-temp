import pytest
from httpie.plugins.base import FormatterPlugin, BasePlugin


def test_formatter_plugin_initialization():
    """Verify that FormatterPlugin stores initialization arguments correctly."""
    plugin = FormatterPlugin(format_options={'indent': 2}, extra='value')
    assert plugin.enabled is True
    assert plugin.kwargs == {'format_options': {'indent': 2}, 'extra': 'value'}
    assert plugin.format_options == {'indent': 2}
    # BasePlugin attributes should be inherited but not overridden
    assert isinstance(plugin, BasePlugin)
    assert plugin.name is None
    assert plugin.description is None
    assert plugin.package_name is None


def test_formatter_plugin_identity_methods():
    """Ensure that identity methods return the input unchanged."""
    plugin = FormatterPlugin(format_options={})
    headers = "Content-Type: application/json\n"
    body = '{"key":"value"}'
    metadata = "Request: GET /api\n"
    assert plugin.format_headers(headers) == headers
    assert plugin.format_body(body, "application/json") == body
    assert plugin.format_metadata(metadata) == metadata


def test_formatter_plugin_error_on_missing_format_options():
    """Creating a FormatterPlugin without 'format_options' should raise a KeyError."""
    with pytest.raises(KeyError):
        FormatterPlugin()  # missing required 'format_options' key
