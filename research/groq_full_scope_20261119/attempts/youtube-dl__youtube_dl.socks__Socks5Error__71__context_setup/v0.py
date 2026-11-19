import socket
import pytest
from youtube_dl.socks import Socks5Error, ProxyError


def test_socks5_error_known_code():
    """Socks5Error should map known error codes to the correct message."""
    err = Socks5Error(code=Socks5Error.ERR_GENERAL_FAILURE)
    # The message should come from the CODES mapping
    assert isinstance(err, Socks5Error)
    assert isinstance(err, ProxyError)
    assert isinstance(err, socket.error)
    assert err.args[0] == Socks5Error.ERR_GENERAL_FAILURE
    assert err.args[1] == Socks5Error.CODES[Socks5Error.ERR_GENERAL_FAILURE]


def test_socks5_error_unknown_code_and_custom_message():
    """When an unknown code is supplied, the message defaults to 'unknown error',
    but a custom message can override it."""
    unknown_code = 0x99
    err_default = Socks5Error(code=unknown_code)
    assert err_default.args[0] == unknown_code
    assert err_default.args[1] == 'unknown error'

    custom_msg = "Custom error message"
    err_custom = Socks5Error(code=unknown_code, msg=custom_msg)
    assert err_custom.args[0] == unknown_code
    assert err_custom.args[1] == custom_msg


def test_socks5_error_inherits_socket_error_and_proxy_error():
    """Socks5Error should be an instance of both socket.error and ProxyError."""
    err = Socks5Error(code=0x02)
    # socket.error is the base class of ProxyError
    assert isinstance(err, socket.error)
    assert isinstance(err, ProxyError)
    # The error code and message should be accessible via args
    assert err.args[0] == 0x02
    assert err.args[1] == Socks5Error.CODES[0x02]
