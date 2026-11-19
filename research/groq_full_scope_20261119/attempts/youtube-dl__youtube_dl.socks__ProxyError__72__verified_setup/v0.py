import socket
import pytest
from youtube_dl.socks import ProxyError

def test_proxy_error_initialization_with_code_and_msg():
    """ProxyError should store the provided code and message."""
    err = ProxyError(0x01, "Custom error message")
    assert isinstance(err, ProxyError)
    assert isinstance(err, socket.error)
    # The args tuple of socket.error contains (code, msg)
    assert err.args == (0x01, "Custom error message")
    # The message should be accessible via str()
    assert str(err) == "Custom error message"

def test_proxy_error_initialization_with_code_only():
    """When only a code is provided, ProxyError should look up the message."""
    # Use a known code from the CODES mapping if available; otherwise test fallback
    # The mapping is not exposed, so we test the fallback for an unknown code.
    unknown_code = 0xFF
    err = ProxyError(unknown_code)
    # The message should be 'unknown error' because the code is not in CODES
    assert err.args == (unknown_code, "unknown error")
    assert str(err) == "unknown error"

def test_proxy_error_default_initialization_and_constant():
    """ProxyError with no arguments should default to ERR_SUCCESS and empty message."""
    err = ProxyError()
    # Default code should be None, message should be empty string
    assert err.args == (None, "")
    assert str(err) == ""
    # The class constant ERR_SUCCESS should be accessible and equal to 0x00
    assert ProxyError.ERR_SUCCESS == 0x00
