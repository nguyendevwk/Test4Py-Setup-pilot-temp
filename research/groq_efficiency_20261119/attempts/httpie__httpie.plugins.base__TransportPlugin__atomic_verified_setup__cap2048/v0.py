import pytest
from httpie.plugins.base import TransportPlugin


class DummyAdapter:
    """Simple stand‑in for a requests adapter."""
    def __init__(self, name: str):
        self.name = name


class ConcreteTransportPlugin(TransportPlugin):
    """Concrete implementation for testing purposes."""
    prefix = "http://example.com"

    def get_adapter(self) -> DummyAdapter:
        return DummyAdapter("dummy")


def test_concrete_plugin_returns_adapter():
    """A concrete plugin should return an adapter instance."""
    plugin = ConcreteTransportPlugin()
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter)
    assert adapter.name == "dummy"


def test_plugin_prefix_attribute():
    """The plugin's prefix attribute should be accessible and correct."""
    plugin = ConcreteTransportPlugin()
    assert plugin.prefix == "http://example.com"


def test_base_plugin_raises_not_implemented():
    """Calling get_adapter on the base class must raise NotImplementedError."""
    base = TransportPlugin()
    with pytest.raises(NotImplementedError):
        base.get_adapter()
