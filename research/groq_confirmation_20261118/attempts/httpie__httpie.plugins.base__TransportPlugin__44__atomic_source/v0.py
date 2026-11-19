import pytest
from httpie.plugins.base import TransportPlugin


class DummyAdapter:
    """Simple stand‑in for a requests adapter."""
    def __init__(self, name: str):
        self.name = name


class ConcreteTransportPlugin(TransportPlugin):
    """Concrete implementation for testing purposes."""
    prefix = "http://example.com/"

    def get_adapter(self):
        return DummyAdapter("dummy")


def test_transport_plugin_base_raises():
    """Base TransportPlugin should raise NotImplementedError when get_adapter is called."""
    plugin = TransportPlugin()
    with pytest.raises(NotImplementedError):
        plugin.get_adapter()


def test_concrete_transport_plugin_returns_adapter():
    """Concrete implementation should return an instance of DummyAdapter."""
    plugin = ConcreteTransportPlugin()
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter)
    assert adapter.name == "dummy"


def test_transport_plugin_prefix_attribute():
    """The prefix attribute should be accessible and match the expected value."""
    plugin = ConcreteTransportPlugin()
    assert plugin.prefix == "http://example.com/"
