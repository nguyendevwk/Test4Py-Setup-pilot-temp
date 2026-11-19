import pytest
from httpie.plugins.base import TransportPlugin, BasePlugin


def test_default_prefix_is_none():
    """The base TransportPlugin should expose a prefix attribute set to None."""
    plugin = TransportPlugin()
    assert plugin.prefix is None, "Default prefix should be None"


def test_get_adapter_raises_not_implemented():
    """Calling get_adapter on the base class must raise NotImplementedError."""
    plugin = TransportPlugin()
    with pytest.raises(NotImplementedError):
        plugin.get_adapter()


def test_subclass_can_override_get_adapter_and_prefix():
    """A subclass can provide a concrete adapter and a custom prefix."""
    class DummyAdapter:
        pass

    class CustomTransportPlugin(TransportPlugin):
        prefix = "custom://"

        def get_adapter(self):
            return DummyAdapter()

    plugin = CustomTransportPlugin()
    assert plugin.prefix == "custom://", "Subclass should override prefix"
    adapter = plugin.get_adapter()
    assert isinstance(adapter, DummyAdapter), "get_adapter should return DummyAdapter instance"
