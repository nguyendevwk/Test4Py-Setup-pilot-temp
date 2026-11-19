import pytest
from httpie.plugins.base import TransportPlugin


class DummyAdapter:
    """Simple stand‑in for a requests adapter."""
    def __init__(self, name: str):
        self.name = name


class ConcreteTransport(TransportPlugin):
    """Concrete implementation for testing."""
    prefix = "http://example.com/"

    def get_adapter(self):
        return DummyAdapter("dummy")


def test_base_plugin_raises_not_implemented():
    """TransportPlugin.get_adapter must raise NotImplementedError."""
    plugin = TransportPlugin()
    with pytest.raises(NotImplementedError):
        plugin.get_adapter()


def test_concrete_plugin_prefix_and_adapter():
    """ConcreteTransport should expose the correct prefix and adapter."""
    plugin = ConcreteTransport()
    assert plugin.prefix == "http://example.com/"
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter)
    assert adapter.name == "dummy"


def test_prefix_default_none_on_base():
    """The base class should have prefix set to None by default."""
    plugin = TransportPlugin()
    assert plugin.prefix is None
