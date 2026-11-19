import socket
import pytest
from youtube_dl.socks import ProxyError


def test_proxy_error_inherits_socket_error_and_has_success_code():
    """ProxyError should inherit from socket.error and expose ERR_SUCCESS."""
    assert issubclass(ProxyError, socket.error)
    assert ProxyError.ERR_SUCCESS == 0x00


def test_proxy_error_initialization_with_code_and_message():
    """Initializing with a code and a custom message should set the args correctly."""
    code = 42
    message = "Custom error message"
    err = ProxyError(code, message)
    # socket.error stores the arguments in the .args tuple
    assert err.args == (code, message)
    # The string representation should include the message
    assert str(err) == f"{code}: {message}"


def test_proxy_error_initialization_with_code_only_uses_coded_message_or_unknown():
    """If only a code is provided, the message should come from CODES or default to 'unknown error'."""
    # Use a code that is unlikely to be in CODES
    code = 9999
    err = ProxyError(code)
    # Since CODES is not defined in this module, the fallback should be 'unknown error'
    assert err.args == (code, 'unknown error')
    assert str(err) == f"{code}: unknown error"
