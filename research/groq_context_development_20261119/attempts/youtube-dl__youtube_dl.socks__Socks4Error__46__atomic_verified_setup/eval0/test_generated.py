import pytest
from youtube_dl.socks import Socks4Error, ProxyError

def test_socks4_error_known_code():
    """Socks4Error should map known error codes to the correct message."""
    err = Socks4Error(91)
    assert isinstance(err, Socks4Error)
    assert isinstance(err, ProxyError)
    assert err.args[0] == 91
    assert err.args[1] == 'request rejected or failed'

def test_socks4_error_unknown_code():
    """Socks4Error should default to 'unknown error' for unknown codes."""
    err = Socks4Error(999)
    assert err.args[0] == 999
    assert err.args[1] == 'unknown error'

def test_socks4_error_err_success_constant():
    """Socks4Error should expose the correct success code constant."""
    assert Socks4Error.ERR_SUCCESS == 90
