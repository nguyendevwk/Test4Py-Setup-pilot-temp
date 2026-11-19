import pytest
from httpie.plugins.base import BasePlugin


def test_default_attributes():
    """BasePlugin should expose default class attributes."""
    assert BasePlugin.name is None
    assert BasePlugin.description is None
    assert BasePlugin.package_name is None


def test_attribute_assignment_and_inheritance():
    """Assigning attributes on a subclass should not affect the base class."""
    class CustomPlugin(BasePlugin):
        name = "Custom"
        description = "A custom plugin"

    # Subclass attributes
    assert CustomPlugin.name == "Custom"
    assert CustomPlugin.description == "A custom plugin"
    assert CustomPlugin.package_name is None

    # Base class remains unchanged
    assert BasePlugin.name is None
    assert BasePlugin.description is None
    assert BasePlugin.package_name is None


def test_instance_attribute_overrides_class_attribute():
    """Instance attributes should override class attributes."""
    class OverridePlugin(BasePlugin):
        name = "Override"

    plugin = OverridePlugin()
    # Instance attribute overrides class attribute
    plugin.name = "InstanceOverride"
    assert plugin.name == "InstanceOverride"
    # Class attribute remains unchanged
    assert OverridePlugin.name == "Override"
