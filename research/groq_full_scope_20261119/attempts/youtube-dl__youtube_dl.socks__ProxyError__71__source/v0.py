import socket
import pytest
from youtube_dl.socks import ProxyError


def test_proxy_error_with_code_and_msg():
    """ProxyError should store the provided code and message."""
    code = 42
    msg = "custom error message"
    err = ProxyError(code, msg)
    # socket.error stores args as (code, msg)
    assert err.args == (code, msg)
    # The string representation should include the message
    assert str(err) == f"{code}: {msg}"


def test_proxy_error_code_only_uses_mapping_or_default():
    """When only a code is provided, ProxyError should use the CODES mapping
    if present, otherwise default to 'unknown error'."""
    # Determine if the module defines a CODES mapping
    codes = getattr(ProxyError, "CODES", {})
    # Pick a code that is unlikely to be in the mapping
    test_code = 9999
    if test_code in codes:
        expected_msg = codes[test_code]
    else:
        expected_msg = "unknown error"
    err = ProxyError(test_code)
    assert err.args == (test_code, expected_msg)
    assert str(err) == f"{test_code}: {expected_msg}"


def test_proxy_error_inherits_socket_error():
    """ProxyError should be a subclass of socket.error."""
    err = ProxyError(0, "no error")
    assert isinstance(err, socket.error)
    # Also ensure that the error can be caught as a socket.error
    try:
        raise err
    except socket.error as e:
        assert e is err
