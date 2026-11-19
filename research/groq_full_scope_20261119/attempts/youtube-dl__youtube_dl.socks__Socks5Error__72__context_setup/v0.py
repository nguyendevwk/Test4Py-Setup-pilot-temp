import pytest
import socket
from youtube_dl.socks import Socks5Error, ProxyError

def test_socks5_error_default_message():
    """Socks5Error should use the predefined message for known codes."""
    err = Socks5Error(code=Socks5Error.ERR_GENERAL_FAILURE)
    assert isinstance(err, Socks5Error)
    assert isinstance(err, ProxyError)
    assert isinstance(err, socket.error)
    # The message should come from the CODES mapping
    assert err.args[1] == Socks5Error.CODES[Socks5Error.ERR_GENERAL_FAILURE]
    # The error code should be stored as the first argument
    assert err.args[0] == Socks5Error.ERR_GENERAL_FAILURE

def test_socks5_error_unknown_code():
    """Unknown error codes should default to 'unknown error'."""
    unknown_code = 0x99
    err = Socks5Error(code=unknown_code)
    assert err.args[0] == unknown_code
    assert err.args[1] == 'unknown error'

def test_socks5_error_custom_message_overrides():
    """Providing a custom message should override the default lookup."""
    custom_msg = "Custom failure message"
    err = Socks5Error(code=Socks5Error.ERR_GENERAL_FAILURE, msg=custom_msg)
    assert err.args[0] == Socks5Error.ERR_GENERAL_FAILURE
    assert err.args[1] == custom_msg
