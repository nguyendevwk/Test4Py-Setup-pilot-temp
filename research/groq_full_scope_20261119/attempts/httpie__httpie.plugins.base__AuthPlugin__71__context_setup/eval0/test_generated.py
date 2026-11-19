import pytest
from httpie.plugins.base import AuthPlugin, BasePlugin


class DummyAuth(AuthPlugin):
    """Concrete implementation for testing purposes."""
    def get_auth(self, username=None, password=None):
        return f"auth({username!r},{password!r})"


def test_dummy_auth_returns_expected_value():
    """Verify that the concrete implementation returns the expected string."""
    plugin = DummyAuth()
    result = plugin.get_auth("user", "pass")
    assert result == "auth('user','pass')"


def test_default_attributes_of_auth_plugin():
    """Ensure that the default class attributes are set as documented."""
    plugin = DummyAuth()
    assert plugin.auth_type is None
    assert plugin.auth_require is True
    assert plugin.auth_parse is True
    assert plugin.netrc_parse is False
    assert plugin.prompt_password is True
    assert plugin.raw_auth is None


def test_base_plugin_get_auth_raises_not_implemented():
    """Calling get_auth on the abstract base class should raise NotImplementedError."""
    with pytest.raises(NotImplementedError):
        BasePlugin().get_auth()
