import pytest
from httpie.plugins.base import TransportPlugin, BasePlugin


def test_transport_plugin_initialization():
    """TransportPlugin should inherit BasePlugin and expose default attributes."""
    plugin = TransportPlugin()
    # Inheritance check
    assert isinstance(plugin, BasePlugin)
    # Default attributes
    assert plugin.prefix is None
    assert plugin.name is None
    assert plugin.description is None
    assert plugin.package_name is None


def test_transport_plugin_prefix_boundary():
    """The prefix attribute should remain None until explicitly set."""
    plugin = TransportPlugin()
    # Ensure prefix is None initially
    assert plugin.prefix is None
    # Setting a custom prefix should update the attribute
    plugin.prefix = "http://example.com"
    assert plugin.prefix == "http://example.com"


def test_transport_plugin_get_adapter_raises():
    """Calling get_adapter on TransportPlugin should raise NotImplementedError."""
    plugin = TransportPlugin()
    with pytest.raises(NotImplementedError):
        plugin.get_adapter()
