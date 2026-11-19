import pytest
from httpie.plugins.base import BasePlugin


def test_default_attributes():
    """BasePlugin should expose default class attributes."""
    assert BasePlugin.name is None
    assert BasePlugin.description is None
    assert BasePlugin.package_name is None


def test_attribute_assignment_and_inheritance(tmp_path):
    """Assigning attributes on a subclass should not affect the base class."""
    class CustomPlugin(BasePlugin):
        name = "Custom"
        description = "A custom plugin"
        package_name = "custom_pkg"

    # Subclass attributes
    assert CustomPlugin.name == "Custom"
    assert CustomPlugin.description == "A custom plugin"
    assert CustomPlugin.package_name == "custom_pkg"

    # Base class remains unchanged
    assert BasePlugin.name is None
    assert BasePlugin.description is None
    assert BasePlugin.package_name is None


def test_instance_attribute_overrides_class_attribute(tmp_path):
    """Instance attributes should override class attributes."""
    class OverridePlugin(BasePlugin):
        name = "Override"

    plugin_instance = OverridePlugin()
    # Instance attribute overrides class attribute
    plugin_instance.name = "InstanceOverride"
    assert plugin_instance.name == "InstanceOverride"
    # Class attribute remains unchanged
    assert OverridePlugin.name == "Override"
