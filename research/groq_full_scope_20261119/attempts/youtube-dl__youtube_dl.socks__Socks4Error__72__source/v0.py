import pytest
from youtube_dl.socks import Socks4Error

def test_success_code_attribute():
    """Socks4Error should expose the success code as a class attribute."""
    assert hasattr(Socks4Error, "ERR_SUCCESS")
    assert Socks4Error.ERR_SUCCESS == 90

def test_known_error_message():
    """When instantiated with a known error code, the exception message should match the mapping."""
    err = Socks4Error(91)
    # The message should contain the human‑readable description from CODES
    assert "request rejected or failed" in str(err)
    # The error code should be accessible via the instance (if defined)
    if hasattr(err, "code"):
        assert err.code == 91

def test_unknown_error_message():
    """Instantiating with an unknown error code should still produce a meaningful message."""
    unknown_code = 999
    err = Socks4Error(unknown_code)
    # The message should indicate an unknown error
    assert "Unknown error" in str(err) or str(unknown_code) in str(err)
