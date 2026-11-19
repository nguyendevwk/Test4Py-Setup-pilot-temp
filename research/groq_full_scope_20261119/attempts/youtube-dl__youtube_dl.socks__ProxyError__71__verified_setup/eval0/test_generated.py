import pytest
import socket
from youtube_dl.socks import ProxyError

def test_proxy_error_default_message():
    """When only a code is supplied, the message comes from CODES or defaults to 'unknown error'."""
    # Use a code that is unlikely to be in CODES to trigger the default
    code = 9999
    err = ProxyError(code=code)
    # The message should be the default string
    assert str(err) == 'unknown error'
    # The error code should be stored in the args tuple
    assert err.args[0] == code
    # It should still be a subclass of socket.error
    assert isinstance(err, socket.error)

def test_proxy_error_known_code():
    """When a known code is supplied, the message is taken from CODES."""
    # Pick a code that is known to exist in the CODES mapping
    known_code = next(iter(ProxyError.CODES))
    expected_msg = ProxyError.CODES[known_code]
    err = ProxyError(code=known_code)
    assert str(err) == expected_msg
    assert err.args[0] == known_code

def test_proxy_error_custom_message():
    """When both code and custom message are supplied, the custom message overrides the mapping."""
    code = 42
    custom_msg = "Custom error message"
    err = ProxyError(code=code, msg=custom_msg)
    assert str(err) == custom_msg
    assert err.args[0] == code
