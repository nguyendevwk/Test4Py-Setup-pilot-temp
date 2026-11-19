import pytest
from httpie.plugins.base import AuthPlugin


def test_default_attributes():
    """AuthPlugin should expose the expected default class attributes."""
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


def test_raw_auth_stays_none_when_not_set():
    """raw_auth should remain None until explicitly set."""
    plugin = AuthPlugin()
    assert plugin.raw_auth is None
    # Setting raw_auth to a value should persist
    plugin.raw_auth = "user:pass"
    assert plugin.raw_auth == "user:pass"
