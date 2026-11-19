import pytest
from httpie.plugins.base import AuthPlugin


def test_default_attributes():
    """Verify that the default class attributes match the specification."""
    plugin = AuthPlugin()
    assert plugin.auth_type is None
    assert plugin.auth_require is True
    assert plugin.auth_parse is True
    assert plugin.netrc_parse is False
    assert plugin.prompt_password is True
    assert plugin.raw_auth is None


def test_get_auth_raises_not_implemented():
    """get_auth should raise NotImplementedError when not overridden."""
    plugin = AuthPlugin()
    with pytest.raises(NotImplementedError):
        plugin.get_auth()
    with pytest.raises(NotImplementedError):
        plugin.get_auth(username="user", password="pass")


def test_raw_auth_assignment_and_access(tmp_path):
    """raw_auth should reflect the value passed during initialization."""
    # Simulate passing a raw auth string by setting the attribute manually
    plugin = AuthPlugin()
    raw_value = "user:pass"
    plugin.raw_auth = raw_value
    assert plugin.raw_auth == raw_value
    # Ensure that get_auth still raises NotImplementedError even with raw_auth set
    with pytest.raises(NotImplementedError):
        plugin.get_auth(username="user", password="pass")
