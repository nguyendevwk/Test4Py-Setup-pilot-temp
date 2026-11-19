import re
import pytest
from httpie.output.processing import Conversion
from httpie.plugins import ConverterPlugin
from httpie.plugins.registry import plugin_manager
from httpie.context import Environment

# Helper to create a dummy converter plugin class
class DummyConverter(ConverterPlugin):
    def __init__(self, mime: str):
        self.mime = mime

    @classmethod
    def supports(cls, mime: str) -> bool:
        return mime == "application/json"

    def convert(self, data):
        return f"converted:{data}"


def test_get_converter_returns_instance_for_supported_mime(monkeypatch):
    # Arrange: monkeypatch plugin_manager to return our dummy converter
    monkeypatch.setattr(plugin_manager, "get_converters", lambda: [DummyConverter])
    # Act
    converter = Conversion.get_converter("application/json")
    # Assert
    assert converter is not None
    assert isinstance(converter, DummyConverter)
    assert converter.mime == "application/json"
    # Verify conversion works as expected
    assert converter.convert("payload") == "converted:payload"


def test_get_converter_returns_none_for_unsupported_mime(monkeypatch):
    # Arrange: monkeypatch plugin_manager to return our dummy converter
    monkeypatch.setattr(plugin_manager, "get_converters", lambda: [DummyConverter])
    # Act
    converter = Conversion.get_converter("text/plain")
    # Assert
    assert converter is None


def test_get_converter_returns_none_for_invalid_mime(monkeypatch):
    # Arrange: monkeypatch plugin_manager to return our dummy converter
    monkeypatch.setattr(plugin_manager, "get_converters", lambda: [DummyConverter])
    # Act
    converter = Conversion.get_converter("invalid/mime")
    # Assert
    assert converter is None
