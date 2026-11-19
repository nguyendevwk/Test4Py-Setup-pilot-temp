import re
import pytest
from httpie.output.processing import Conversion
from httpie.plugins import ConverterPlugin
from httpie.plugins.registry import plugin_manager
from httpie.context import Environment

# Helper dummy plugin
class DummyConverter(ConverterPlugin):
    def __init__(self, mime: str):
        self.mime = mime

    @classmethod
    def supports(cls, mime: str) -> bool:
        return mime == "application/dummy"

    def convert(self, data):
        return f"converted:{data}"

def test_get_converter_returns_instance_for_valid_mime(tmp_path):
    # Register dummy converter
    plugin_manager.register(DummyConverter)
    # Ensure the environment is set up (if needed)
    env = Environment()
    # Call get_converter with a MIME type that the dummy supports
    converter = Conversion.get_converter("application/dummy")
    assert converter is not None
    assert isinstance(converter, DummyConverter)
    assert converter.mime == "application/dummy"
    # Clean up
    plugin_manager.unregister(DummyConverter)

def test_get_converter_returns_none_for_invalid_mime(tmp_path):
    # Ensure no converter is registered for this MIME
    converter = Conversion.get_converter("application/unknown")
    assert converter is None

def test_get_converter_returns_none_when_no_plugin_supports(tmp_path):
    # Register a converter that does not support the MIME
    class NonMatchingConverter(ConverterPlugin):
        @classmethod
        def supports(cls, mime: str) -> bool:
            return False
        def convert(self, data):
            return data
    plugin_manager.register(NonMatchingConverter)
    converter = Conversion.get_converter("application/json")
    assert converter is None
    plugin_manager.unregister(NonMatchingConverter)
