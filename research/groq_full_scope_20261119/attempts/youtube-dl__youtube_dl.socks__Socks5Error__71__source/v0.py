import pytest
from youtube_dl.socks import Socks5Error

def test_socks5_error_constants():
    # The error code for general failure should be 0x01
    assert Socks5Error.ERR_GENERAL_FAILURE == 0x01
    # The CODES mapping should contain the expected key-value pairs
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

def test_socks5_error_message():
    # Instantiate the error with a known code and verify the message
    err = Socks5Error(0x05)
    # The string representation should include the human‑readable description
    assert 'Connection refused' in str(err)
    # The error code should be stored as an attribute if ProxyError implements it
    # (common pattern: self.code = code)
    assert getattr(err, 'code', None) == 0x05

def test_socks5_error_unknown_code():
    # Using an unknown code should still create an error instance
    unknown_code = 0x99
    err = Socks5Error(unknown_code)
    # The message should indicate an unknown error code
    assert 'unknown' in str(err).lower()
    # The code attribute should reflect the unknown code
    assert getattr(err, 'code', None) == unknown_code
