import pytest
from youtube_dl.socks import Socks5Auth

def test_socks5_auth_constants_exist_and_correct():
    """Socks5Auth should expose the expected authentication constants."""
    assert hasattr(Socks5Auth, "AUTH_NONE")
    assert hasattr(Socks5Auth, "AUTH_GSSAPI")
    assert hasattr(Socks5Auth, "AUTH_USER_PASS")
    assert hasattr(Socks5Auth, "AUTH_NO_ACCEPTABLE")

    assert Socks5Auth.AUTH_NONE == 0x00
    assert Socks5Auth.AUTH_GSSAPI == 0x01
    assert Socks5Auth.AUTH_USER_PASS == 0x02
    assert Socks5Auth.AUTH_NO_ACCEPTABLE == 0xFF

def test_socks5_auth_constant_types():
    """All authentication constants should be integers."""
    for name in ("AUTH_NONE", "AUTH_GSSAPI", "AUTH_USER_PASS", "AUTH_NO_ACCEPTABLE"):
        value = getattr(Socks5Auth, name)
        assert isinstance(value, int), f"{name} is not an int"

def test_socks5_auth_instantiation_and_identity():
    """Instantiating Socks5Auth should create a distinct object with no state."""
    instance1 = Socks5Auth()
    instance2 = Socks5Auth()
    # Instances should be distinct objects
    assert instance1 is not instance2
    # They should not have any attributes beyond those defined on the class
    assert set(instance1.__dict__) == set()
    assert set(instance2.__dict__) == set()
