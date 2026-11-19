import pytest
from httpie.plugins.base import TransportPlugin
from requests.adapters import BaseAdapter


class DummyAdapter(BaseAdapter):
    """Simple adapter stub for testing purposes."""
    pass


class DummyTransportPlugin(TransportPlugin):
    """Concrete implementation of TransportPlugin for testing."""
    prefix = "http://example.com"

    def get_adapter(self):
        return DummyAdapter()


def test_transport_plugin_get_adapter_returns_adapter_instance():
    """TransportPlugin subclass should return an adapter instance."""
    plugin = DummyTransportPlugin()
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter), "Adapter should be an instance of DummyAdapter"
    assert isinstance(adapter, BaseAdapter), "Adapter should be a subclass of BaseAdapter"


def test_transport_plugin_prefix_attribute():
    """The prefix attribute should be preserved as defined."""
    plugin = DummyTransportPlugin()
    assert plugin.prefix == "http://example.com", "Prefix should match the defined value"


def test_transport_plugin_base_raises_not_implemented():
    """Calling get_adapter on the base TransportPlugin should raise NotImplementedError."""
    base_plugin = TransportPlugin()
    with pytest.raises(NotImplementedError):
        base_plugin.get_adapter()
