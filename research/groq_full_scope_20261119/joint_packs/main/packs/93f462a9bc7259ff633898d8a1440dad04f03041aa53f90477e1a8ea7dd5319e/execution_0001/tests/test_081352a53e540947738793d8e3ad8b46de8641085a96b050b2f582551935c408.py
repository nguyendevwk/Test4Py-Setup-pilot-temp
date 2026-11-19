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


def test_concrete_plugin_returns_adapter_and_prefix():
    """A concrete plugin should expose its prefix and return an adapter instance."""
    plugin = ConcreteTransportPlugin()
    # The prefix attribute should be the value defined in the subclass.
    assert plugin.prefix == "http://example.com/"
    # get_adapter should return an instance of DummyAdapter.
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter)
    assert adapter.name == "dummy"


def test_base_plugin_get_adapter_raises_not_implemented():
    """Calling get_adapter on the abstract base class must raise NotImplementedError."""
    base = TransportPlugin()
    with pytest.raises(NotImplementedError):
        base.get_adapter()


def test_subclass_can_override_prefix_and_adapter():
    """A subclass can change the prefix and provide a custom adapter."""
    class CustomPlugin(TransportPlugin):
        prefix = "https://custom/"

        def get_adapter(self):
            return DummyAdapter("custom")

    plugin = CustomPlugin()
    assert plugin.prefix == "https://custom/"
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter)
    assert adapter.name == "custom"
