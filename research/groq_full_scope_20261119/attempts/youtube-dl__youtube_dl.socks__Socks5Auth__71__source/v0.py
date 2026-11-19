import pytest
import importlib
import inspect

# Import the target module
socks_module = importlib.import_module("youtube_dl.socks")
Socks5Auth = socks_module.Socks5Auth

def test_socks5auth_constants():
    """Verify that the authentication constants are defined correctly."""
    assert hasattr(Socks5Auth, "AUTH_NONE")
    assert hasattr(Socks5Auth, "AUTH_GSSAPI")
    assert hasattr(Socks5Auth, "AUTH_USER_PASS")
    assert hasattr(Socks5Auth, "AUTH_NO_ACCEPTABLE")
    assert Socks5Auth.AUTH_NONE == 0x00
    assert Socks5Auth.AUTH_GSSAPI == 0x01
    assert Socks5Auth.AUTH_USER_PASS == 0x02
    assert Socks5Auth.AUTH_NO_ACCEPTABLE == 0xFF

def test_socks5auth_build_auth_request_valid():
    """When building a valid authentication request, the output should be a bytes object
    starting with the correct version and method identifiers."""
    # The method should exist; if not, the test will fail.
    assert hasattr(Socks5Auth, "build_auth_request")
    # Build a request for USER_PASS authentication
    request = Socks5Auth.build_auth_request(Socks5Auth.AUTH_USER_PASS)
    assert isinstance(request, bytes)
    # The first byte is the SOCKS version (0x05)
    assert request[0] == 0x05
    # The second byte is the authentication method (0x02 for USER_PASS)
    assert request[1] == Socks5Auth.AUTH_USER_PASS

def test_socks5auth_build_auth_request_invalid():
    """Providing an unsupported authentication method should raise a ValueError."""
    # The method should exist; if not, the test will fail.
    assert hasattr(Socks5Auth, "build_auth_request")
    with pytest.raises(ValueError):
        Socks5Auth.build_auth_request(0x99)  # 0x99 is not a defined method
