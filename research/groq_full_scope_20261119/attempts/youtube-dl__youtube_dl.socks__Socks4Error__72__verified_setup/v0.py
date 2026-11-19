import pytest
from youtube_dl.socks import Socks4Error

def test_socks4error_success_code_and_constants():
    """Verify that the success code constant is correct and that an instance
    created with the success code has the expected attributes."""
    err = Socks4Error(code=Socks4Error.ERR_SUCCESS)
    assert err.code == 90
    assert err.msg is None
    # The CODES mapping should not contain the success code
    assert 90 not in Socks4Error.CODES

def test_socks4error_known_error_message():
    """Verify that known error codes map to the correct human‑readable message
    and that the instance stores the message passed to the constructor."""
    err = Socks4Error(code=91, msg="Custom message")
    assert err.code == 91
    assert err.msg == "Custom message"
    # The CODES mapping should provide the default description for the code
    assert Socks4Error.CODES[91] == 'request rejected or failed'

def test_socks4error_unknown_code_behavior():
    """Verify that an unknown error code does not raise an exception and that
    the instance still stores the provided code and message."""
    unknown_code = 999
    err = Socks4Error(code=unknown_code, msg="Unknown error")
    assert err.code == unknown_code
    assert err.msg == "Unknown error"
    # The CODES mapping should not contain the unknown code
    assert unknown_code not in Socks4Error.CODES
