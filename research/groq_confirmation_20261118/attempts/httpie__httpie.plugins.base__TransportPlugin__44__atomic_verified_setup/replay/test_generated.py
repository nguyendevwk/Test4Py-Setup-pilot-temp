import pytest
from httpie.plugins.base import TransportPlugin


def test_transport_plugin_default_prefix():
    """The base TransportPlugin should expose a default prefix of None."""
    plugin = TransportPlugin()
    assert plugin.prefix is None, "Default prefix should be None"


def test_transport_plugin_get_adapter_raises():
    """Calling get_adapter on the base class must raise NotImplementedError."""
    plugin = TransportPlugin()
    with pytest.raises(NotImplementedError):
        plugin.get_adapter()


def test_transport_plugin_subclass_get_adapter_returns_instance():
    """A subclass that implements get_adapter should return an adapter instance."""
    class DummyAdapter:
        pass

    class DummyPlugin(TransportPlugin):
        prefix = "dummy://"

        def get_adapter(self):
            return DummyAdapter()

    plugin = DummyPlugin()
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter), "Adapter should be an instance of DummyAdapter"
    assert plugin.prefix == "dummy://", "Subclass should override prefix correctly"
