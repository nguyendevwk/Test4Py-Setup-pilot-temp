import pytest
from httpie.plugins.base import TransportPlugin
from requests.adapters import BaseAdapter


def test_default_prefix_is_none():
    """The base TransportPlugin should expose a default prefix of None."""
    assert TransportPlugin.prefix is None


def test_get_adapter_raises_not_implemented():
    """Calling get_adapter on the base class should raise NotImplementedError."""
    plugin = TransportPlugin()
    with pytest.raises(NotImplementedError):
        plugin.get_adapter()


def test_subclass_can_implement_get_adapter_and_set_prefix():
    """A subclass can provide an adapter and set a custom prefix."""
    class DummyAdapter(BaseAdapter):
        pass

    class DummyTransportPlugin(TransportPlugin):
        prefix = "http://example.com"

        def get_adapter(self):
            return DummyAdapter()

    plugin = DummyTransportPlugin()
    assert plugin.prefix == "http://example.com"
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter)
