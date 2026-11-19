import pytest
from youtube_dl.socks import Socks4Error, ProxyError

def test_socks4_error_success_code():
    """Socks4Error should expose the success code from ProxyError."""
    assert Socks4Error.ERR_SUCCESS == ProxyError.ERR_SUCCESS
    assert Socks4Error.ERR_SUCCESS == 0x00

def test_socks4_error_known_codes():
    """Known error codes should map to the correct messages."""
    for code, expected_msg in Socks4Error.CODES.items():
        err = Socks4Error(code=code)
        # The message should be the mapped string
        assert str(err) == f"{code}: {expected_msg}"
        # The underlying socket error code should be the same
        assert err.args[0] == code
        assert err.args[1] == expected_msg

def test_socks4_error_unknown_code():
    """An unknown error code should default to 'unknown error'."""
    unknown_code = 999
    err = Socks4Error(code=unknown_code)
    assert err.args[0] == unknown_code
    assert err.args[1] == 'unknown error'
    assert str(err) == f"{unknown_code}: unknown error"
