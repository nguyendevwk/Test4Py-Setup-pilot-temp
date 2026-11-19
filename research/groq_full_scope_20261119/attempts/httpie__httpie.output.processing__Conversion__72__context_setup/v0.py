import re
import pytest
from httpie.output.processing import Conversion, is_valid_mime, MIME_RE
from httpie.plugins import ConverterPlugin
from httpie.plugins.registry import plugin_manager


class DummyConverter(ConverterPlugin):
    """A minimal ConverterPlugin implementation for testing."""
    def __init__(self, mime: str):
        self.mime = mime

    @classmethod
    def supports(cls, mime: str) -> bool:
        return mime == "text/plain"

    def convert(self, data):
        return data


def test_get_converter_valid_mime_returns_instance(monkeypatch):
    """When a valid MIME type is supported, get_converter returns an instance."""
    # Arrange: monkeypatch plugin_manager to return our DummyConverter
    monkeypatch.setattr(plugin_manager, "get_converters", lambda: [DummyConverter])

    # Act
    converter = Conversion.get_converter("text/plain")

    # Assert
    assert converter is not None
    assert isinstance(converter, DummyConverter)
    assert converter.mime == "text/plain"


def test_get_converter_invalid_mime_returns_none(monkeypatch):
    """When the MIME type is syntactically invalid, get_converter returns None."""
    # Arrange: monkeypatch plugin_manager to return DummyConverter (won't be used)
    monkeypatch.setattr(plugin_manager, "get_converters", lambda: [DummyConverter])

    # Act
    converter = Conversion.get_converter("invalid-mime")

    # Assert
    assert converter is None


def test_get_converter_supported_but_not_found_returns_none(monkeypatch):
    """When the MIME type is valid but no converter supports it, get_converter returns None."""
    # Arrange: monkeypatch plugin_manager to return a converter that does not support the MIME
    class UnsupportedConverter(ConverterPlugin):
        @classmethod
        def supports(cls, mime: str) -> bool:
            return False

        def __init__(self, mime: str):
            self.mime = mime

        def convert(self, data):
            return data

    monkeypatch.setattr(plugin_manager, "get_converters", lambda: [UnsupportedConverter])

    # Act
    converter = Conversion.get_converter("application/json")

    # Assert
    assert converter is None
