import textwrap
import pytest
from httpie.cli.definition import format_auth_help
from httpie.plugins.builtin import BuiltinAuthPlugin

class DummyAuthPlugin:
    auth_type = "dummy"
    name = "Dummy Auth"
    package_name = "dummy_pkg"
    description = "A dummy authentication plugin used for testing."

class AnotherAuthPlugin:
    auth_type = "another"
    name = "Another Auth"
    package_name = "another_pkg"
    description = "Another plugin with a longer description that should wrap properly when displayed in the help text."

class BuiltinDummyAuthPlugin(BuiltinAuthPlugin):
    auth_type = "builtin"
    name = "Builtin Auth"
    package_name = "builtin_pkg"
    description = "Builtin authentication plugin."

@pytest.fixture
def auth_mapping():
    return {
        "dummy": DummyAuthPlugin,
        "another": AnotherAuthPlugin,
        "builtin": BuiltinDummyAuthPlugin,
    }

def test_format_auth_help_includes_all_plugins_and_wraps_description(auth_mapping):
    help_text = format_auth_help(auth_mapping, isolation_mode=False)
    # Default auth type should be the first plugin in the mapping
    assert "Defaults to \"dummy\"" in help_text
    # All plugin types should appear
    assert '"dummy": Dummy Auth' in help_text
    assert '"another": Another Auth' in help_text
    assert '"builtin": Builtin Auth' in help_text
    # Description of another plugin should be wrapped to a maximum width of 80
    wrapped = textwrap.wrap(AnotherAuthPlugin.description, width=80)
    for line in wrapped:
        assert line in help_text
    # No isolation mode message should be present
    assert "run:\n\n    $ http --auth-type" not in help_text

def test_format_auth_help_isolation_mode_excludes_non_builtin(auth_mapping):
    help_text = format_auth_help(auth_mapping, isolation_mode=True)
    # Only builtin plugins should be listed
    assert '"builtin": Builtin Auth' in help_text
    assert '"dummy": Dummy Auth' not in help_text
    assert '"another": Another Auth' not in help_text
    # Isolation mode message should be present
    assert "run:\n\n    $ http --auth-type" in help_text

def test_format_auth_help_handles_empty_mapping():
    with pytest.raises(IndexError):
        format_auth_help({}, isolation_mode=False)
