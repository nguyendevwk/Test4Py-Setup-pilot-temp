import pytest
from youtube_dl.socks import Socks4Error

def test_socks4_error_success_code_and_message():
    """Socks4Error should expose the success code and map known error codes to messages."""
    # Success code constant
    assert Socks4Error.ERR_SUCCESS == 90

    # Known error code mapping
    err = Socks4Error(91)
    assert err.code == 91
    assert str(err) == 'request rejected or failed'

    # Unknown error code should not raise and should keep the code
    unknown_err = Socks4Error(99)
    assert unknown_err.code == 99
    # The string representation for unknown codes falls back to the code itself
    assert str(unknown_err) == '99'


def test_socks4_error_codelist_access_and_default():
    """CODES dict should provide correct messages and return None for missing keys."""
    # Known codes
    for code, message in Socks4Error.CODES.items():
        assert Socks4Error.CODES[code] == message

    # Missing key returns None
    assert Socks4Error.CODES.get(100) is None
    assert Socks4Error.CODES.get(0) is None


def test_socks4_error_initialization_and_repr():
    """Initialization should store the code and message correctly, and repr should be informative."""
    err = Socks4Error(92, "Custom message")
    # Code and message are stored
    assert err.code == 92
    assert err.msg == "Custom message"

    # __repr__ should include class name and code
    rep = repr(err)
    assert rep.startswith("<Socks4Error")
    assert "92" in rep
    assert "Custom message" in rep
