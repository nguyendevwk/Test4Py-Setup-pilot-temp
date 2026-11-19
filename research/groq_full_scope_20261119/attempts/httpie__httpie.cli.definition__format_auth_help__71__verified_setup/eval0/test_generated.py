import textwrap
import pytest
from httpie.cli.definition import format_auth_help
from httpie.plugins.builtin import BuiltinAuthPlugin


class DummyAuthPlugin:
    auth_type = "dummy"
    name = "Dummy Auth"
    package_name = "dummy_pkg"
    description = None


class DummyAuthPluginWithDesc:
    auth_type = "desc"
    name = "Desc Auth"
    package_name = "desc_pkg"
    description = "This is a very long description that should be wrapped across multiple lines to test the wrapping logic in the format_auth_help function."


class BuiltinDummyAuthPlugin(BuiltinAuthPlugin):
    auth_type = "builtin"
    name = "Builtin Auth"
    package_name = "builtin_pkg"
    description = "Builtin description."


def test_format_auth_help_includes_all_plugins_and_default():
    plugins = {
        "dummy": DummyAuthPlugin,
        "builtin": BuiltinDummyAuthPlugin,
    }
    help_text = format_auth_help(plugins)
    # Default should be the first plugin's auth_type
    assert "Defaults to \"dummy\"" in help_text
    # Both plugins should be listed
    assert '"dummy": Dummy Auth' in help_text
    assert '"builtin": Builtin Auth' in help_text
    # Builtin plugin should not show package name
    assert "(provided by" not in help_text
    # Non-builtin plugin should show package name
    assert "(provided by dummy_pkg)" in help_text


def test_format_auth_help_with_isolation_mode_filters_plugins_and_shows_command():
    plugins = {
        "dummy": DummyAuthPlugin,
        "builtin": BuiltinDummyAuthPlugin,
    }
    help_text = format_auth_help(plugins, isolation_mode=True)
    # Only builtin plugin should appear
    assert '"builtin": Builtin Auth' in help_text
    assert '"dummy": Dummy Auth' not in help_text
    # The command suggestion should be present
    assert "$ http --auth-type" in help_text
    # The default should still be the first plugin in the filtered list
    assert "Defaults to \"builtin\"" in help_text


def test_format_auth_help_wraps_long_description():
    plugins = {"desc": DummyAuthPluginWithDesc}
    help_text = format_auth_help(plugins)
    # The description should be wrapped and indented
    wrapped = textwrap.wrap(DummyAuthPluginWithDesc.description, width=70)
    for line in wrapped:
        assert line in help_text
    # Indentation should be present
    assert "      " in help_text
    # The description should not be truncated
    assert "very long description" in help_text
