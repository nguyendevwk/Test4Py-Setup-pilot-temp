import pytest
from httpie.plugins.base import AuthPlugin, BasePlugin

class DummyAuthPlugin(AuthPlugin):
    """Concrete implementation for testing purposes."""
    auth_type = "dummy"
    auth_require = False

    def get_auth(self, username: str = None, password: str = None):
        # Return a simple tuple to represent auth credentials
        return (username, password)


def test_dummy_auth_plugin_returns_expected_tuple():
    """Test that DummyAuthPlugin.get_auth returns the expected tuple."""
    plugin = DummyAuthPlugin()
    # Simulate parsed credentials
    result = plugin.get_auth(username="user", password="pass")
    assert result == ("user", "pass")
    # raw_auth should be None when credentials are parsed
    assert plugin.raw_auth is None


def test_auth_plugin_without_credentials_when_not_required():
    """Test that plugin can be instantiated without credentials when auth_require is False."""
    plugin = DummyAuthPlugin()
    # Even without passing username/password, get_auth should return (None, None)
    result = plugin.get_auth()
    assert result == (None, None)
    # Ensure auth_type is set correctly
    assert plugin.auth_type == "dummy"


def test_auth_plugin_abstract_get_auth_raises_not_implemented():
    """Test that calling get_auth on the base class raises NotImplementedError."""
    base_plugin = AuthPlugin()
    with pytest.raises(NotImplementedError):
        base_plugin.get_auth()
