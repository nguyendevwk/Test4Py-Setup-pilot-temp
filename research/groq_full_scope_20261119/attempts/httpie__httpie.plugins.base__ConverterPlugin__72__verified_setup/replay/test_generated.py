import pytest
from httpie.plugins.base import ConverterPlugin


def test_converter_plugin_initialization():
    """ConverterPlugin should store the provided MIME type."""
    plugin = ConverterPlugin("application/json")
    assert plugin.mime == "application/json"


def test_converter_plugin_convert_raises():
    """Calling convert on the base class should raise NotImplementedError."""
    plugin = ConverterPlugin("text/plain")
    with pytest.raises(NotImplementedError):
        plugin.convert(b"data")


def test_converter_plugin_supports_raises():
    """Calling supports on the base class should raise NotImplementedError."""
    with pytest.raises(NotImplementedError):
        ConverterPlugin.supports("application/octet-stream")
