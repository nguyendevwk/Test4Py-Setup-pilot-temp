import pytest
from youtube_dl.socks import Socks5Error

def test_socks5_error_default_message_and_code():
    """Socks5Error should store the provided code and message."""
    err = Socks5Error(code=0x01, msg="test failure")
    assert err.code == 0x01
    assert err.msg == "test failure"
    # The string representation should include the message
    assert str(err) == "test failure"

def test_socks5_error_code_mapping():
    """The CODES mapping should contain all expected error descriptions."""
    expected_codes = {
        0x01: 'general SOCKS server failure',
        0x02: 'connection not allowed by ruleset',
        0x03: 'Network unreachable',
        0x04: 'Host unreachable',
        0x05: 'Connection refused',
        0x06: 'TTL expired',
        0x07: 'Command not supported',
        0x08: 'Address type not supported',
        0xFE: 'unknown username or invalid password',
        0xFF: 'all offered authentication methods were rejected'
    }
    assert Socks5Error.CODES == expected_codes
    # Verify that each code maps to the correct description
    for code, description in expected_codes.items():
        assert Socks5Error.CODES[code] == description

def test_socks5_error_invalid_code_handling():
    """Creating a Socks5Error with an unknown code should not raise an exception."""
    # Unknown code not in CODES
    unknown_code = 0xAB
    err = Socks5Error(code=unknown_code, msg="unknown error")
    assert err.code == unknown_code
    assert err.msg == "unknown error"
    # The string representation should still be the message
    assert str(err) == "unknown error"
