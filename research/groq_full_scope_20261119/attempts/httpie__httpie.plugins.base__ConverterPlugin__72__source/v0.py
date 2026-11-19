import pytest
from httpie.plugins.base import ConverterPlugin


def test_converter_plugin_initialization():
    """ConverterPlugin should store the provided MIME type."""
    plugin = ConverterPlugin("application/octet-stream")
    assert plugin.mime == "application/octet-stream"


def test_convert_raises_not_implemented():
    """Calling convert on the base class must raise NotImplementedError."""
    plugin = ConverterPlugin("application/octet-stream")
    with pytest.raises(NotImplementedError):
        plugin.convert(b"data")


def test_supports_raises_not_implemented():
    """Calling supports on the base class must raise NotImplementedError."""
    with pytest.raises(NotImplementedError):
        ConverterPlugin.supports("application/octet-stream")
