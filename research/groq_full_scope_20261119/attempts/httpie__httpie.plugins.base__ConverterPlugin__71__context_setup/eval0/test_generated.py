import pytest
from httpie.plugins.base import ConverterPlugin, BasePlugin


class DummyConverter(ConverterPlugin):
    """Concrete implementation for testing purposes."""

    def __init__(self, mime: str):
        super().__init__(mime)

    def convert(self, body: bytes) -> tuple[str, str]:
        # Simple echo converter that pretends to convert binary to text
        return ("text/plain", body.decode("utf-8"))

    @classmethod
    def supports(cls, mime: str) -> bool:
        # Supports only MIME types that start with "text/"
        return mime.startswith("text/")


def test_abstract_methods_raise_not_implemented():
    """Ensure that the base class methods raise NotImplementedError."""
    plugin = ConverterPlugin("application/octet-stream")
    with pytest.raises(NotImplementedError):
        plugin.convert(b"data")
    with pytest.raises(NotImplementedError):
        ConverterPlugin.supports("application/octet-stream")


def test_dummy_converter_supports_and_convert():
    """Verify that DummyConverter correctly reports support and converts data."""
    assert DummyConverter.supports("text/plain") is True
    assert DummyConverter.supports("application/json") is False

    body = b"hello world"
    content_type, content = DummyConverter("text/plain").convert(body)
    assert content_type == "text/plain"
    assert content == "hello world"


def test_converter_plugin_initialization_and_attributes():
    """Check that the plugin stores the MIME type and inherits BasePlugin attributes."""
    plugin = DummyConverter("text/plain")
    assert plugin.mime == "text/plain"
    # BasePlugin defines class attributes; they should be accessible
    assert hasattr(plugin, "name") and plugin.name is None
    assert hasattr(plugin, "description") and plugin.description is None
    assert hasattr(plugin, "package_name") and plugin.package_name is None
