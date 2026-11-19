import pytest
from httpie.plugins.base import TransportPlugin


class DummyTransportPlugin(TransportPlugin):
    """Concrete implementation for testing purposes."""
    prefix = "dummy://"

    def get_adapter(self):
        return "adapter_instance"


def test_default_prefix_is_none():
    """The base class should have a default prefix of None."""
    assert TransportPlugin.prefix is None


def test_get_adapter_raises_not_implemented():
    """Calling get_adapter on the base class must raise NotImplementedError."""
    with pytest.raises(NotImplementedError):
        TransportPlugin().get_adapter()


def test_subclass_get_adapter_returns_value(tmp_path):
    """A subclass that implements get_adapter should return the expected value."""
    plugin = DummyTransportPlugin()
    adapter = plugin.get_adapter()
    assert adapter == "adapter_instance"
    assert plugin.prefix == "dummy://"
