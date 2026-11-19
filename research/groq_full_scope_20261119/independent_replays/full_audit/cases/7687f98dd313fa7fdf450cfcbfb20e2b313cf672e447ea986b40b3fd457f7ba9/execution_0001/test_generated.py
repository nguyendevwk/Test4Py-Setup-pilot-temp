import pytest
from httpie.plugins.base import FormatterPlugin, BasePlugin


def test_formatter_plugin_initialization_and_attributes():
    """Verify that the plugin is initialized correctly and attributes are set."""
    plugin = FormatterPlugin(format_options={"indent": 2}, other="value")
    assert plugin.enabled is True
    assert plugin.kwargs == {"format_options": {"indent": 2}, "other": "value"}
    assert plugin.format_options == {"indent": 2}
    # BasePlugin attributes should be inherited
    assert isinstance(plugin, BasePlugin)
    assert plugin.name is None
    assert plugin.description is None
    assert plugin.package_name is None


def test_formatter_plugin_missing_format_options_raises():
    """Ensure that missing 'format_options' in kwargs raises a KeyError."""
    with pytest.raises(KeyError):
        FormatterPlugin(other="value")  # format_options key is required


def test_formatter_plugin_identity_methods():
    """Check that format_* methods return the input unchanged."""
    plugin = FormatterPlugin(format_options={})
    headers = "Content-Type: application/json\n"
    body = '{"key": "value"}'
    metadata = "Response time: 123ms"

    assert plugin.format_headers(headers) == headers
    assert plugin.format_body(body, "application/json") == body
    assert plugin.format_metadata(metadata) == metadata
