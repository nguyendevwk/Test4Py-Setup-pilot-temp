import pytest
from httpie.plugins.base import BasePlugin


def test_default_attributes():
    """BasePlugin should expose default attributes set to None."""
    plugin = BasePlugin()
    assert plugin.name is None
    assert plugin.description is None
    assert plugin.package_name is None


def test_modify_instance_attributes(tmp_path):
    """Instance attributes can be modified independently of the class."""
    plugin = BasePlugin()
    plugin.name = "Auth"
    plugin.description = "Test authentication plugin"
    plugin.package_name = "httpie.plugins.auth"

    assert plugin.name == "Auth"
    assert plugin.description == "Test authentication plugin"
    assert plugin.package_name == "httpie.plugins.auth"

    # Ensure the class attributes remain unchanged
    assert BasePlugin.name is None
    assert BasePlugin.description is None
    assert BasePlugin.package_name is None

    # Use tmp_path to create a temporary file as required by the test guidelines
    temp_file = tmp_path / "plugin_info.txt"
    temp_file.write_text(f"{plugin.name}\n{plugin.description}\n{plugin.package_name}")
    assert temp_file.read_text() == "Auth\nTest authentication plugin\nhttpie.plugins.auth\n"


def test_class_attribute_inheritance_and_isolation():
    """Subclassing should inherit default attributes, and changes are isolated."""
    class CustomPlugin(BasePlugin):
        pass

    # Subclass inherits the default None values
    custom = CustomPlugin()
    assert custom.name is None
    assert custom.description is None
    assert custom.package_name is None

    # Changing subclass attributes does not affect the base class
    custom.name = "Custom"
    assert custom.name == "Custom"
    assert BasePlugin.name is None

    # Changing base class attributes does not affect the subclass instance
    BasePlugin.description = "Base description"
    assert BasePlugin.description == "Base description"
    assert custom.description is None
