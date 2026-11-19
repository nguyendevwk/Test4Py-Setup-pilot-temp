import pytest
from httpie.plugins.base import BasePlugin


def test_default_attributes():
    """BasePlugin should expose default class attributes."""
    assert BasePlugin.name is None
    assert BasePlugin.description is None
    assert BasePlugin.package_name is None


def test_setting_attributes_on_instance():
    """Instance attributes can be overridden without affecting the class."""
    plugin = BasePlugin()
    plugin.name = "Custom Plugin"
    plugin.description = "A test plugin"
    plugin.package_name = "httpie.plugins.test"

    # Instance values
    assert plugin.name == "Custom Plugin"
    assert plugin.description == "A test plugin"
    assert plugin.package_name == "httpie.plugins.test"

    # Class values remain unchanged
    assert BasePlugin.name is None
    assert BasePlugin.description is None
    assert BasePlugin.package_name is None


def test_subclass_inheritance_and_override():
    """Subclasses inherit defaults and can override them."""
    class MyPlugin(BasePlugin):
        name = "MyPlugin"
        description = "Handles custom auth"

    # Class attributes on subclass
    assert MyPlugin.name == "MyPlugin"
    assert MyPlugin.description == "Handles custom auth"
    assert MyPlugin.package_name is None

    # Instance inherits subclass defaults
    instance = MyPlugin()
    assert instance.name == "MyPlugin"
    assert instance.description == "Handles custom auth"
    assert instance.package_name is None

    # Override on instance
    instance.package_name = "httpie.plugins.myplugin"
    assert instance.package_name == "httpie.plugins.myplugin"
    # Subclass class attribute remains unchanged
    assert MyPlugin.package_name is None
