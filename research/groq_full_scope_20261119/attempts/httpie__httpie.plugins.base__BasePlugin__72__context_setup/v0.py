import pytest
from httpie.plugins.base import BasePlugin


def test_default_attributes():
    """BasePlugin should expose default attributes as None."""
    plugin = BasePlugin()
    assert plugin.name is None, "Default name should be None"
    assert plugin.description is None, "Default description should be None"
    assert plugin.package_name is None, "Default package_name should be None"


def test_setting_name_and_description():
    """Assigning name and description should update the attributes."""
    plugin = BasePlugin()
    plugin.name = "Test Plugin"
    plugin.description = "A plugin for testing."
    assert plugin.name == "Test Plugin", "Name should reflect the assigned value"
    assert plugin.description == "A plugin for testing.", "Description should reflect the assigned value"


def test_setting_package_name():
    """Assigning package_name should update the attribute."""
    plugin = BasePlugin()
    plugin.package_name = "httpie.plugins.test"
    assert plugin.package_name == "httpie.plugins.test", "package_name should reflect the assigned value"
