import pytest
from httpie.plugins.base import AuthPlugin


def test_default_attributes():
    """AuthPlugin should expose the documented default configuration values."""
    plugin = AuthPlugin()
    assert plugin.auth_type is None
    assert plugin.auth_require is True
    assert plugin.auth_parse is True
    assert plugin.netrc_parse is False
    assert plugin.prompt_password is True
    assert plugin.raw_auth is None


def test_get_auth_raises_not_implemented():
    """Calling get_auth on the base class must raise NotImplementedError."""
    plugin = AuthPlugin()
    with pytest.raises(NotImplementedError):
        plugin.get_auth()


def test_subclass_can_override_get_auth():
    """A subclass can provide a concrete implementation of get_auth."""
    class DummyAuthPlugin(AuthPlugin):
        def get_auth(self, username=None, password=None):
            return f"auth:{username}:{password}"

    plugin = DummyAuthPlugin()
    result = plugin.get_auth("user", "pass")
    assert result == "auth:user:pass"
