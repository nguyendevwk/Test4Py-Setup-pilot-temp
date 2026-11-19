import re
import pytest
from httpie.output.processing import Conversion, is_valid_mime, MIME_RE
from httpie.plugins import ConverterPlugin
from httpie.plugins.registry import plugin_manager


class DummyConverter(ConverterPlugin):
    """A minimal ConverterPlugin that claims to support a specific MIME type."""
    def __init__(self, mime: str):
        self.mime = mime

    @classmethod
    def supports(cls, mime: str) -> bool:
        return mime == "application/dummy"

    def convert(self, data):
        return f"converted:{data}"


def test_get_converter_returns_instance_for_supported_mime(monkeypatch):
    """When a valid MIME type is supported, get_converter returns an instance."""
    # Arrange: monkeypatch the plugin manager to return our dummy converter
    monkeypatch.setattr(plugin_manager, "get_converters", lambda: [DummyConverter])

    # Act
    converter = Conversion.get_converter("application/dummy")

    # Assert
    assert converter is not None
    assert isinstance(converter, DummyConverter)
    assert converter.mime == "application/dummy"
    # Verify that the converter behaves as expected
    assert converter.convert("foo") == "converted:foo"


def test_get_converter_returns_none_for_invalid_mime(monkeypatch):
    """When the MIME type is syntactically invalid, get_converter returns None."""
    # Arrange: ensure plugin manager is called (though it should not be)
    called = {"count": 0}
    def fake_get_converters():
        called["count"] += 1
        return [DummyConverter]
    monkeypatch.setattr(plugin_manager, "get_converters", fake_get_converters)

    # Act
    converter = Conversion.get_converter("invalid-mime")

    # Assert
    assert converter is None
    # The plugin manager should not have been queried
    assert called["count"] == 0


def test_get_converter_returns_none_when_no_converter_supports_mime(monkeypatch):
    """When no registered converter supports the MIME type, get_converter returns None."""
    # Arrange: monkeypatch to return a converter that does not support the MIME
    class UnsupportedConverter(ConverterPlugin):
        @classmethod
        def supports(cls, mime: str) -> bool:
            return False

        def __init__(self, mime: str):
            self.mime = mime

    monkeypatch.setattr(plugin_manager, "get_converters", lambda: [UnsupportedConverter])

    # Act
    converter = Conversion.get_converter("application/json")

    # Assert
    assert converter is None
