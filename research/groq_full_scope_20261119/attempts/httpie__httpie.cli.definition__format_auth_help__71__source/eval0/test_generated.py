import textwrap
import pytest
from httpie.cli.definition import format_auth_help
from httpie.plugins.builtin import BuiltinAuthPlugin


class DummyAuthPlugin:
    auth_type = "dummy"
    name = "Dummy Auth"
    package_name = "dummy_pkg"
    description = "This is a dummy authentication plugin used for testing purposes."

class DummyBuiltinAuthPlugin(BuiltinAuthPlugin):
    auth_type = "builtin"
    name = "Builtin Auth"
    description = ""


def test_format_auth_help_includes_all_plugins_and_default():
    plugins = {"dummy": DummyAuthPlugin, "builtin": DummyBuiltinAuthPlugin}
    result = format_auth_help(plugins)
    # Default should be the first plugin's auth_type
    assert "Defaults to \"dummy\"" in result
    # Both plugins should be listed
    assert '"dummy": Dummy Auth' in result
    assert '"builtin": Builtin Auth' in result
    # Dummy plugin should mention its package
    assert "(provided by dummy_pkg)" in result
    # Dummy plugin description should be wrapped and indented
    wrapped_desc = "\n      ".join(textwrap.wrap(DummyAuthPlugin.description))
    assert wrapped_desc in result
    # No isolation message should be present
    assert "To see all available auth types" not in result


def test_format_auth_help_isolation_mode_filters_non_builtin():
    plugins = {"dummy": DummyAuthPlugin, "builtin": DummyBuiltinAuthPlugin}
    result = format_auth_help(plugins, isolation_mode=True)
    # Only builtin plugin should appear
    assert '"builtin": Builtin Auth' in result
    assert '"dummy": Dummy Auth' not in result
    # Isolation message should be present
    assert "To see all available auth types" in result
    # Default should be builtin
    assert "Defaults to \"builtin\"" in result


def test_format_auth_help_handles_empty_description_and_no_package():
    class NoDescPlugin(BuiltinAuthPlugin):
        auth_type = "nodec"
        name = "No Description"
        description = ""

    plugins = {"nodec": NoDescPlugin}
    result = format_auth_help(plugins)
    # No description block should appear
    assert "No Description" in result
    assert "provided by" not in result
    assert "\n      " not in result
    # Default should be nodec
    assert "Defaults to \"nodec\"" in result
