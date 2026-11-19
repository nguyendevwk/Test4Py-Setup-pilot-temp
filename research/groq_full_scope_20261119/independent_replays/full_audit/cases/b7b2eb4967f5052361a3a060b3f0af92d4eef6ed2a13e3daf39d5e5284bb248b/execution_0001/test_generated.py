import pytest
from httpie.plugins.base import TransportPlugin


class DummyTransportPlugin(TransportPlugin):
    """Concrete implementation for testing purposes."""
    prefix = "dummy://"

    def get_adapter(self):
        return "adapter_instance"


def test_default_prefix_is_none():
    """The base class should expose a default prefix of None."""
    assert TransportPlugin.prefix is None


def test_get_adapter_raises_not_implemented():
    """Calling get_adapter on the abstract base should raise NotImplementedError."""
    with pytest.raises(NotImplementedError):
        TransportPlugin().get_adapter()


def test_subclass_overrides_get_adapter_and_prefix():
    """A subclass must override prefix and get_adapter correctly."""
    plugin = DummyTransportPlugin()
    assert plugin.prefix == "dummy://"
    assert plugin.get_adapter() == "adapter_instance"
