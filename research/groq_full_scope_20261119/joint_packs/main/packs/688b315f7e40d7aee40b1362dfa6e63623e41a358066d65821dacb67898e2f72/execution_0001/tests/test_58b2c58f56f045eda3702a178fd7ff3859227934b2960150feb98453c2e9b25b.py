import pytest
from httpie.output.processing import Conversion
from httpie.plugins.registry import plugin_manager
from httpie.plugins import ConverterPlugin

# Dummy converter plugin for testing
class DummyConverter(ConverterPlugin):
    supports_mime = "application/json"

    def __init__(self, mime: str):
        self.mime = mime

    @classmethod
    def supports(cls, mime: str) -> bool:
        return mime == cls.supports_mime

# Helper to monkeypatch plugin_manager.get_converters
@pytest.fixture(autouse=True)
def patch_plugin_manager(monkeypatch):
    monkeypatch.setattr(plugin_manager, "get_converters", lambda: [DummyConverter])

def test_get_converter_returns_instance_for_valid_mime():
    """Conversion.get_converter should return a DummyConverter instance when the MIME is supported."""
    converter = Conversion.get_converter("application/json")
    assert converter is not None
    assert isinstance(converter, DummyConverter)
    assert converter.mime == "application/json"

def test_get_converter_returns_none_for_unsupported_mime():
    """Conversion.get_converter should return None when the MIME is not supported by any converter."""
    converter = Conversion.get_converter("text/plain")
    assert converter is None

def test_get_converter_handles_invalid_mime_format():
    """Conversion.get_converter should return None for an invalid MIME format (e.g., missing slash)."""
    converter = Conversion.get_converter("invalidmime")
    assert converter is None
