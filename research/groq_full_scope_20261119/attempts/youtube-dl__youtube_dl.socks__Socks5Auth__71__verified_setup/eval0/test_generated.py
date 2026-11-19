import pytest
from youtube_dl.socks import Socks5Auth


def test_socks5auth_constants():
    """Verify that the authentication constants have the expected values."""
    assert Socks5Auth.AUTH_NONE == 0x00
    assert Socks5Auth.AUTH_GSSAPI == 0x01
    assert Socks5Auth.AUTH_USER_PASS == 0x02
    assert Socks5Auth.AUTH_NO_ACCEPTABLE == 0xFF


def test_socks5auth_instance_attributes():
    """An instance of Socks5Auth should expose the same constants as class attributes."""
    instance = Socks5Auth()
    assert instance.AUTH_NONE == 0x00
    assert instance.AUTH_GSSAPI == 0x01
    assert instance.AUTH_USER_PASS == 0x02
    assert instance.AUTH_NO_ACCEPTABLE == 0xFF


def test_socks5auth_invalid_attribute():
    """Accessing a non‑existent attribute should raise AttributeError."""
    instance = Socks5Auth()
    with pytest.raises(AttributeError):
        _ = instance.NON_EXISTENT_ATTRIBUTE
