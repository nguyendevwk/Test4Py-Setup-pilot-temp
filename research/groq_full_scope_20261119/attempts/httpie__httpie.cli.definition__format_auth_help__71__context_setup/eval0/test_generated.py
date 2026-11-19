import textwrap
import pytest
from httpie.cli.definition import format_auth_help
from httpie.plugins.builtin import BuiltinAuthPlugin

# Helper plugin classes for testing
class DummyAuthPlugin:
    auth_type = "dummy"
    name = "Dummy Auth"
    package_name = "dummy_pkg"
    description = "A simple dummy authentication plugin used for testing."

class AnotherAuthPlugin:
    auth_type = "another"
    name = "Another Auth"
    package_name = "another_pkg"
    description = "Another plugin with a longer description that should wrap across multiple lines when displayed in the help text."

class NoDescAuthPlugin:
    auth_type = "nodec"
    name = "No Description Auth"
    package_name = "nodec_pkg"
    description = ""

def test_format_auth_help_basic():
    """Test that the help text includes the default auth type and all plugin entries."""
    mapping = {
        "dummy": DummyAuthPlugin,
        "another": AnotherAuthPlugin,
    }
    help_text = format_auth_help(mapping)
    # Default should be the first plugin's auth_type
    assert "Defaults to \"dummy\"" in help_text
    # Both plugins should appear
    assert '"dummy": Dummy Auth' in help_text
    assert '"another": Another Auth' in help_text
    # Description of dummy plugin should be wrapped correctly
    wrapped = textwrap.wrap(DummyAuthPlugin.description)
    for line in wrapped:
        assert line in help_text
    # No extra isolation mode text
    assert "To see all available auth types" not in help_text

def test_format_auth_help_isolation_mode():
    """Test that isolation_mode filters out non-builtin plugins and adds the extra instruction."""
    mapping = {
        "dummy": DummyAuthPlugin,
        "builtin": BuiltinAuthPlugin,
    }
    help_text = format_auth_help(mapping, isolation_mode=True)
    # Only builtin plugin should be listed
    assert '"builtin":' in help_text
    assert '"dummy":' not in help_text
    # The instruction about running http --auth-type should appear
    assert "run:\n\n    $ http --auth-type" in help_text

def test_format_auth_help_no_description_and_wrapping():
    """Test that plugins without a description are handled correctly and long descriptions wrap."""
    mapping = {
        "nodec": NoDescAuthPlugin,
        "another": AnotherAuthPlugin,
    }
    help_text = format_auth_help(mapping)
    # No description block for NoDescAuthPlugin
    assert '"nodec": No Description Auth' in help_text
    assert 'provided by' not in help_text  # package name should not appear for builtin
    # Long description should be wrapped
    wrapped = textwrap.wrap(AnotherAuthPlugin.description)
    for line in wrapped:
        assert line in help_text
