import pytest
from httpie.plugins.base import AuthPlugin
from requests.auth import AuthBase


class DummyAuth(AuthBase):
    """Simple AuthBase subclass used for testing."""
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd

    def __repr__(self):
        return f"<DummyAuth user={self.user!r} pwd={self.pwd!r}>"


class TestAuthPluginImplementation(AuthPlugin):
    """Concrete implementation of AuthPlugin for testing purposes."""
    auth_type = "dummy"

    def get_auth(self, username: str = None, password: str = None):
        # Return a DummyAuth instance using the provided credentials
        return DummyAuth(username, password)


def test_get_auth_raises_not_implemented():
    """AuthPlugin.get_auth should raise NotImplementedError when not overridden."""
    base_plugin = AuthPlugin()
    with pytest.raises(NotImplementedError):
        base_plugin.get_auth("user", "pass")


def test_get_auth_returns_correct_type_and_credentials(tmp_path):
    """Concrete implementation should return a DummyAuth instance with correct attributes."""
    plugin = TestAuthPluginImplementation()
    # Simulate raw auth value
    plugin.raw_auth = "user:pass"
    auth_obj = plugin.get_auth(username="user", password="pass")
    assert isinstance(auth_obj, DummyAuth)
    assert auth_obj.user == "user"
    assert auth_obj.pwd == "pass"
    # Ensure raw_auth is accessible and unchanged
    assert plugin.raw_auth == "user:pass"


def test_get_auth_with_missing_password(tmp_path):
    """When password is omitted, get_auth should still create an auth object with None password."""
    plugin = TestAuthPluginImplementation()
    plugin.raw_auth = "user:"
    auth_obj = plugin.get_auth(username="user", password=None)
    assert isinstance(auth_obj, DummyAuth)
    assert auth_obj.user == "user"
    assert auth_obj.pwd is None
