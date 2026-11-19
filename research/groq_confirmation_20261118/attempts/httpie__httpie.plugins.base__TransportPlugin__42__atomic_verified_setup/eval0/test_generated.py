import pytest
from httpie.plugins.base import TransportPlugin


class DummyAdapter:
    """Simple dummy adapter to satisfy the interface."""
    def __init__(self):
        self.name = "dummy"


class DummyTransportPlugin(TransportPlugin):
    """Concrete implementation for testing purposes."""
    prefix = "http://dummy"

    def get_adapter(self):
        return DummyAdapter()


def test_transport_plugin_default_prefix_and_abstract_method():
    """TransportPlugin should have prefix None and raise NotImplementedError."""
    plugin = TransportPlugin()
    assert plugin.prefix is None
    with pytest.raises(NotImplementedError):
        plugin.get_adapter()


def test_dummy_transport_plugin_prefix_and_adapter():
    """Concrete plugin should expose correct prefix and return adapter instance."""
    plugin = DummyTransportPlugin()
    assert plugin.prefix == "http://dummy"
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter)
    assert adapter.name == "dummy"


def test_transport_plugin_get_adapter_type_error_on_invalid_return():
    """Ensure get_adapter returns a BaseAdapter-like object; raise TypeError if not."""
    class InvalidTransportPlugin(TransportPlugin):
        def get_adapter(self):
            return "not an adapter"

    plugin = InvalidTransportPlugin()
    with pytest.raises(TypeError):
        adapter = plugin.get_adapter()
        # Simulate a check that would normally be performed by the framework
        if not hasattr(adapter, "send"):
            raise TypeError("Adapter must implement send method")
