import pytest
from youtube_dl.socks import Socks5Auth

def test_socks5_auth_constants():
    """Verify that the authentication constants have the expected integer values."""
    assert isinstance(Socks5Auth.AUTH_NONE, int)
    assert isinstance(Socks5Auth.AUTH_GSSAPI, int)
    assert isinstance(Socks5Auth.AUTH_USER_PASS, int)
    assert isinstance(Socks5Auth.AUTH_NO_ACCEPTABLE, int)

    assert Socks5Auth.AUTH_NONE == 0x00
    assert Socks5Auth.AUTH_GSSAPI == 0x01
    assert Socks5Auth.AUTH_USER_PASS == 0x02
    assert Socks5Auth.AUTH_NO_ACCEPTABLE == 0xFF

def test_socks5_auth_value_range():
    """Ensure that the constants fall within the valid byte range (0-255)."""
    for value in (
        Socks5Auth.AUTH_NONE,
        Socks5Auth.AUTH_GSSAPI,
        Socks5Auth.AUTH_USER_PASS,
        Socks5Auth.AUTH_NO_ACCEPTABLE,
    ):
        assert 0 <= value <= 255, f"Value {value} out of byte range"

def test_socks5_auth_repr_and_equality():
    """Check that the class can be instantiated and that its representation is informative."""
    # The class has no __init__ arguments; creating an instance should succeed.
    instance = Socks5Auth()
    # The default representation should include the class name.
    assert instance.__class__.__name__ in repr(instance)
    # Instances are distinct objects.
    another = Socks5Auth()
    assert instance is not another
    # Equality is based on identity; two instances are not equal.
    assert instance != another
