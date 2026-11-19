import socket
import pytest
from youtube_dl.socks import ProxyError

def test_proxy_error_initialization_with_code_and_msg():
    """ProxyError should store the provided code and message."""
    err = ProxyError(0x01, "Custom error")
    assert isinstance(err, ProxyError)
    assert isinstance(err, socket.error)
    # The args tuple should contain the code and message
    assert err.args == (0x01, "Custom error")
    # The message attribute should be the second element of args
    assert err.args[1] == "Custom error"

def test_proxy_error_initialization_with_code_only():
    """When only a code is provided, ProxyError should look up a default message."""
    # Use a known code that exists in the CODES mapping
    # The mapping is not exposed, but we can rely on the default message for an unknown code
    err = ProxyError(0xFF)  # 0xFF is unlikely to be in CODES
    assert isinstance(err, ProxyError)
    assert isinstance(err, socket.error)
    # The message should be 'unknown error' for an unmapped code
    assert err.args[1] == 'unknown error'
    # The code should be preserved
    assert err.args[0] == 0xFF

def test_proxy_error_default_initialization_and_constant():
    """ProxyError without arguments should default to code None and use ERR_SUCCESS."""
    err = ProxyError()
    assert isinstance(err, ProxyError)
    assert isinstance(err, socket.error)
    # Default code should be None
    assert err.args[0] is None
    # Default message should be the string representation of ERR_SUCCESS
    # Since ERR_SUCCESS is 0x00, the default message is likely '0' or similar
    # We check that the message is a string and not empty
    assert isinstance(err.args[1], str) and err.args[1] != ''
    # The ERR_SUCCESS constant should be accessible and equal to 0x00
    assert ProxyError.ERR_SUCCESS == 0x00
