import pytest
from httpie.output.processing import Conversion
from httpie.plugins import ConverterPlugin
from httpie.plugins.registry import plugin_manager
from httpie.context import Environment

# Dummy converter plugin for testing
class DummyConverter(ConverterPlugin):
    def __init__(self, mime: str):
        self.mime = mime

    @classmethod
    def supports(cls, mime: str) -> bool:
        return mime == "application/json"

    def convert(self, data):
        return f"converted:{data}"


def test_get_converter_returns_converter_for_supported_mime(monkeypatch):
    # Arrange: monkeypatch the plugin manager and is_valid_mime
    monkeypatch.setattr(plugin_manager, "get_converters", lambda: [DummyConverter])
    monkeypatch.setattr(Conversion, "is_valid_mime", lambda mime: True)

    # Act
    converter = Conversion.get_converter("application/json")

    # Assert
    assert converter is not None
    assert isinstance(converter, DummyConverter)
    assert converter.mime == "application/json"
    assert converter.convert("foo") == "converted:foo"


def test_get_converter_returns_none_for_unsupported_mime(monkeypatch):
    # Arrange: plugin manager returns a converter that does not support the mime
    class UnsupportedConverter(ConverterPlugin):
        @classmethod
        def supports(cls, mime: str) -> bool:
            return False

        def __init__(self, mime: str):
            self.mime = mime

    monkeypatch.setattr(plugin_manager, "get_converters", lambda: [UnsupportedConverter])
    monkeypatch.setattr(Conversion, "is_valid_mime", lambda mime: True)

    # Act
    converter = Conversion.get_converter("text/plain")

    # Assert
    assert converter is None


def test_get_converter_returns_none_for_invalid_mime(monkeypatch):
    # Arrange: even if a converter exists, invalid mime should return None
    monkeypatch.setattr(plugin_manager, "get_converters", lambda: [DummyConverter])
    monkeypatch.setattr(Conversion, "is_valid_mime", lambda mime: False)

    # Act
    converter = Conversion.get_converter("application/json")

    # Assert
    assert converter is None
