import pytest
from httpie.plugins.base import ConverterPlugin


def test_converter_plugin_initialization_sets_mime():
    """The constructor should store the provided MIME type."""
    plugin = ConverterPlugin("application/json")
    assert plugin.mime == "application/json"


def test_convert_raises_not_implemented_error():
    """Calling convert on the base class should raise NotImplementedError."""
    plugin = ConverterPlugin("text/plain")
    with pytest.raises(NotImplementedError):
        plugin.convert(b"data")


def test_supports_raises_not_implemented_error():
    """Calling supports on the base class should raise NotImplementedError."""
    with pytest.raises(NotImplementedError):
        ConverterPlugin.supports("text/plain")
