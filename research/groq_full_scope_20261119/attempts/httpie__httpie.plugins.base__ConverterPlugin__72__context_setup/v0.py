import pytest
from httpie.plugins.base import ConverterPlugin, BasePlugin


class DummyConverter(ConverterPlugin):
    """Concrete implementation for testing purposes."""

    def convert(self, body: bytes) -> tuple[str, str]:
        # Simple echo converter
        return ("text/plain", body.decode("utf-8"))

    @classmethod
    def supports(cls, mime: str) -> bool:
        return mime == "text/plain"


def test_converter_initialization_and_attributes():
    """Test that the plugin stores the MIME type correctly."""
    plugin = DummyConverter("text/plain")
    assert isinstance(plugin, DummyConverter)
    assert plugin.mime == "text/plain"
    # BasePlugin attributes should be present (even if None)
    assert hasattr(plugin, "name")
    assert hasattr(plugin, "description")
    assert hasattr(plugin, "package_name")


def test_converter_supports_method():
    """Test the supports classmethod returns correct boolean."""
    assert DummyConverter.supports("text/plain") is True
    assert DummyConverter.supports("application/json") is False
    # Ensure it is a classmethod, not instance method
    assert DummyConverter.supports.__func__ is DummyConverter.supports.__func__


def test_converter_convert_raises_on_base_and_works_on_dummy():
    """Test that the base class raises NotImplementedError and the dummy works."""
    base_plugin = ConverterPlugin("application/octet-stream")
    with pytest.raises(NotImplementedError):
        base_plugin.convert(b"data")

    dummy = DummyConverter("text/plain")
    result_type, result_content = dummy.convert(b"hello")
    assert result_type == "text/plain"
    assert result_content == "hello"
