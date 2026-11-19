import pytest
from httpie.plugins.base import TransportPlugin
from requests.adapters import BaseAdapter


class DummyAdapter(BaseAdapter):
    """Simple adapter stub for testing purposes."""
    def send(self, request, **kwargs):
        return None


class DummyTransportPlugin(TransportPlugin):
    """Concrete implementation of TransportPlugin for testing."""
    prefix = "http://dummy"

    def get_adapter(self):
        return DummyAdapter()


def test_default_prefix_is_none():
    """TransportPlugin should have a default prefix of None."""
    assert TransportPlugin.prefix is None


def test_get_adapter_raises_not_implemented():
    """Calling get_adapter on the base class should raise NotImplementedError."""
    with pytest.raises(NotImplementedError):
        TransportPlugin().get_adapter()


def test_custom_plugin_returns_adapter_and_prefix():
    """A concrete subclass should return an adapter instance and have a prefix."""
    plugin = DummyTransportPlugin()
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter)
    assert plugin.prefix == "http://dummy"
