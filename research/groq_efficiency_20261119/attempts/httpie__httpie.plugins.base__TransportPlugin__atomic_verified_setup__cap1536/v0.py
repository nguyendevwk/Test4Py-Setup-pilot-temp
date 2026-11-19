import pytest
from httpie.plugins.base import TransportPlugin
from requests.adapters import BaseAdapter


class DummyAdapter(BaseAdapter):
    """A minimal adapter implementation for testing purposes."""
    def send(self, request, **kwargs):
        return None


class ConcreteTransportPlugin(TransportPlugin):
    """Concrete implementation of TransportPlugin for testing."""
    prefix = "http://example.com"

    def get_adapter(self):
        return DummyAdapter()


def test_concrete_plugin_returns_adapter_and_prefix():
    """Verify that a concrete plugin returns the expected adapter instance and prefix."""
    plugin = ConcreteTransportPlugin()
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter), "Adapter should be an instance of DummyAdapter"
    assert plugin.prefix == "http://example.com", "Prefix should match the defined value"


def test_base_plugin_get_adapter_raises_not_implemented():
    """Ensure that calling get_adapter on the base class raises NotImplementedError."""
    base_plugin = TransportPlugin()
    with pytest.raises(NotImplementedError):
        base_plugin.get_adapter()


def test_plugin_prefix_can_be_none_and_adapter_is_callable():
    """Test that a plugin with prefix set to None still works and its adapter can be called."""
    class NonePrefixPlugin(TransportPlugin):
        prefix = None

        def get_adapter(self):
            return DummyAdapter()

    plugin = NonePrefixPlugin()
    assert plugin.prefix is None, "Prefix should be None"
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter), "Adapter should be an instance of DummyAdapter"
