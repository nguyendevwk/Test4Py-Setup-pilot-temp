import pytest
from youtube_dl.socks import Socks5Auth

def test_socks5_auth_constants():
    """Verify that the authentication constants have the expected values."""
    assert Socks5Auth.AUTH_NONE == 0x00
    assert Socks5Auth.AUTH_GSSAPI == 0x01
    assert Socks5Auth.AUTH_USER_PASS == 0x02
    assert Socks5Auth.AUTH_NO_ACCEPTABLE == 0xFF

def test_socks5_auth_invalid_value():
    """Ensure that creating a Socks5Auth instance with an unsupported auth type raises a ValueError."""
    with pytest.raises(ValueError):
        Socks5Auth(0x03)  # 0x03 is not a defined auth type

def test_socks5_auth_repr_and_str():
    """Check that the __repr__ and __str__ methods return a readable string containing the auth type."""
    auth = Socks5Auth(Socks5Auth.AUTH_USER_PASS)
    rep = repr(auth)
    str_val = str(auth)
    assert "Socks5Auth" in rep
    assert "AUTH_USER_PASS" in rep
    assert rep == str_val
