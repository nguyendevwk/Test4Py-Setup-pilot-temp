import pytest
from youtube_dl.socks import Socks5Error

def test_default_instantiation_and_repr():
    """Socks5Error can be instantiated without arguments and has a default representation."""
    err = Socks5Error()
    # Default code should be None and message should be None
    assert err.code is None
    assert err.msg is None
    # The string representation should include the class name
    assert str(err).startswith("Socks5Error")

def test_known_code_and_message():
    """Providing a known error code and message yields correct attributes and lookup."""
    code = Socks5Error.ERR_GENERAL_FAILURE
    message = "Test failure"
    err = Socks5Error(code=code, msg=message)
    assert err.code == code
    assert err.msg == message
    # The CODES mapping should contain the provided code
    assert code in Socks5Error.CODES
    # The string representation should include the human‑readable description
    assert Socks5Error.CODES[code] in str(err)

def test_unknown_code_handling():
    """An unknown error code is still stored but not present in the CODES mapping."""
    unknown_code = 0x99  # not defined in CODES
    err = Socks5Error(code=unknown_code, msg="Unknown")
    assert err.code == unknown_code
    assert err.msg == "Unknown"
    # The code should not be in the mapping
    assert unknown_code not in Socks5Error.CODES
    # The string representation should still include the numeric code
    assert f"0x{unknown_code:02x}" in str(err)
