import pytest
import socket
from youtube_dl.socks import Socks4Error, ProxyError

def test_known_error_code_message():
    """Socks4Error should map known error codes to the correct message."""
    err = Socks4Error(91)
    # The message should come from the CODES mapping
    assert isinstance(err, Socks4Error)
    assert isinstance(err, ProxyError)
    assert err.args[0] == 91
    assert err.args[1] == Socks4Error.CODES[91]
    # The string representation should include the code and message
    assert str(err) == f"{err.args[0]}: {err.args[1]}"

def test_unknown_error_code_message():
    """Socks4Error should default to 'unknown error' for unmapped codes."""
    err = Socks4Error(999)
    assert isinstance(err, Socks4Error)
    assert err.args[0] == 999
    assert err.args[1] == 'unknown error'
    # Ensure the message is not one of the known codes
    assert err.args[1] not in Socks4Error.CODES.values()

def test_custom_message_overrides_code():
    """Providing a custom message should override the default mapping."""
    custom_msg = "custom error message"
    err = Socks4Error(92, custom_msg)
    assert isinstance(err, Socks4Error)
    assert err.args[0] == 92
    assert err.args[1] == custom_msg
    # The custom message should not be the default mapping
    assert err.args[1] != Socks4Error.CODES[92]
