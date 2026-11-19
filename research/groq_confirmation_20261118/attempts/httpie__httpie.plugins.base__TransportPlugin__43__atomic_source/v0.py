import pytest
from httpie.plugins.base import TransportPlugin


def test_default_prefix_is_none():
    """The base TransportPlugin should expose a prefix attribute set to None."""
    assert TransportPlugin.prefix is None


def test_get_adapter_raises_not_implemented():
    """Calling get_adapter on the base class must raise NotImplementedError."""
    plugin = TransportPlugin()
    with pytest.raises(NotImplementedError):
        plugin.get_adapter()


def test_subclass_implements_get_adapter_and_mount_prefix():
    """A subclass that implements get_adapter should return an adapter instance and set a prefix."""
    class DummyAdapter:
        pass

    class DummyTransportPlugin(TransportPlugin):
        prefix = "dummy://"

        def get_adapter(self):
            return DummyAdapter()

    plugin = DummyTransportPlugin()
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter)
    assert plugin.prefix == "dummy://"
