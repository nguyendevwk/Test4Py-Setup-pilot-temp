import pytest
from httpie.plugins.base import ConverterPlugin
from typing import Tuple


class DummyConverter(ConverterPlugin):
    """Concrete implementation for testing purposes."""

    def convert(self, body: bytes) -> Tuple[str, str]:
        return ("text/plain", body.decode("utf-8"))

    @classmethod
    def supports(cls, mime: str) -> bool:
        return mime == "text/plain"


def test_converter_initialization_and_attributes():
    """Verify that the ConverterPlugin stores the MIME type correctly."""
    plugin = DummyConverter("text/plain")
    assert plugin.mime == "text/plain"


def test_abstract_methods_raise_not_implemented():
    """Ensure that the base class methods raise NotImplementedError."""
    base = ConverterPlugin("application/octet-stream")
    with pytest.raises(NotImplementedError):
        base.convert(b"data")
    with pytest.raises(NotImplementedError):
        ConverterPlugin.supports("application/octet-stream")


def test_dummy_converter_behavior(tmp_path):
    """Test that the concrete DummyConverter works as expected."""
    plugin = DummyConverter("text/plain")
    data = b"Hello, world!"
    content_type, content = plugin.convert(data)
    assert content_type == "text/plain"
    assert content == "Hello, world!"
    # supports should return True only for the matching MIME type
    assert DummyConverter.supports("text/plain") is True
    assert DummyConverter.supports("application/json") is False
