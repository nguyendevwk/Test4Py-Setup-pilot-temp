import pytest
from youtube_dl.socks import Socks5Error

def test_socks5_error_known_code():
    """Socks5Error should map known error codes to human‑readable messages."""
    err = Socks5Error(Socks5Error.ERR_GENERAL_FAILURE)
    # The error message should contain the code and the mapped description
    assert isinstance(err, Socks5Error)
    assert err.args[0] == Socks5Error.ERR_GENERAL_FAILURE
    assert 'general SOCKS server failure' in str(err)

def test_socks5_error_unknown_code():
    """Socks5Error should still be constructible with an unknown code."""
    unknown_code = 0x99
    err = Socks5Error(unknown_code)
    # The error message should include the unknown code in hex form
    assert isinstance(err, Socks5Error)
    assert err.args[0] == unknown_code
    assert f'0x{unknown_code:02x}' in str(err)

def test_socks5_error_codes_dict_integrity():
    """The CODES dictionary should contain all expected keys and values."""
    expected = {
        0x01: 'general SOCKS server failure',
        0x02: 'connection not allowed by ruleset',
        0x03: 'Network unreachable',
        0x04: 'Host unreachable',
        0x05: 'Connection refused',
        0x06: 'TTL expired',
        0x07: 'Command not supported',
        0x08: 'Address type not supported',
        0xFE: 'unknown username or invalid password',
        0xFF: 'all offered authentication methods were rejected',
    }
    assert Socks5Error.CODES == expected
