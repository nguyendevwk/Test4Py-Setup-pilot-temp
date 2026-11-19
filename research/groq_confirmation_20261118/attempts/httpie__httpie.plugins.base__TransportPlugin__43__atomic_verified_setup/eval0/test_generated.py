import pytest
from httpie.plugins.base import TransportPlugin


def test_default_prefix_is_none():
    """The base TransportPlugin should expose a default prefix of None."""
    plugin = TransportPlugin()
    assert plugin.prefix is None, "Default prefix should be None"


def test_get_adapter_raises_not_implemented():
    """Calling get_adapter on the base class must raise NotImplementedError."""
    plugin = TransportPlugin()
    with pytest.raises(NotImplementedError):
        plugin.get_adapter()


def test_custom_plugin_implements_get_adapter_and_prefix():
    """A subclass can override prefix and provide an adapter instance."""
    class DummyAdapter:
        pass

    class CustomPlugin(TransportPlugin):
        prefix = "custom://"

        def get_adapter(self):
            return DummyAdapter()

    plugin = CustomPlugin()
    assert plugin.prefix == "custom://", "Custom prefix should be set correctly"
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter), "Adapter should be an instance of DummyAdapter"
