import pytest
from httpie.plugins.base import BasePlugin


def test_base_plugin_default_attributes():
    """BasePlugin should expose default attributes with None values."""
    plugin = BasePlugin()
    assert plugin.name is None, "Default name should be None"
    assert plugin.description is None, "Default description should be None"
    assert plugin.package_name is None, "Default package_name should be None"


def test_base_plugin_attribute_assignment():
    """Attributes can be set after instantiation."""
    plugin = BasePlugin()
    plugin.name = "Test Plugin"
    plugin.description = "A plugin for testing"
    plugin.package_name = "httpie.plugins.test"
    assert plugin.name == "Test Plugin"
    assert plugin.description == "A plugin for testing"
    assert plugin.package_name == "httpie.plugins.test"


def test_base_plugin_subclass_overrides():
    """Subclassing BasePlugin allows overriding class attributes."""
    class CustomPlugin(BasePlugin):
        name = "Custom"
        description = "Custom description"

    plugin = CustomPlugin()
    assert plugin.name == "Custom"
    assert plugin.description == "Custom description"
    # package_name remains None unless set
    assert plugin.package_name is None
