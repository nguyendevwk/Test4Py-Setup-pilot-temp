import pytest
from youtube_dl.socks import Socks4Error

def test_socks4error_constants():
    """Socks4Error should expose correct constants."""
    # ERR_SUCCESS should be 90
    assert Socks4Error.ERR_SUCCESS == 90
    # CODES should contain expected keys and values
    expected = {
        91: 'request rejected or failed',
        92: 'request rejected because SOCKS server cannot connect to identd on the client',
        93: 'request rejected because the client program and identd report different user-ids'
    }
    assert Socks4Error.CODES == expected

def test_socks4error_initialization_and_str():
    """Instantiating Socks4Error should store code and message correctly."""
    err = Socks4Error(91, "Test message")
    # The instance should store the provided code and message
    assert getattr(err, 'code', None) == 91
    assert getattr(err, 'msg', None) == "Test message"
    # The string representation should include both
    assert "91" in str(err)
    assert "Test message" in str(err)

def test_socks4error_default_message():
    """When no message is provided, the error should use the default from CODES."""
    err = Socks4Error(92)
    # Default message should be the one from CODES mapping
    assert err.msg == Socks4Error.CODES[92]
    # The string representation should contain the default message
    assert "request rejected because SOCKS server cannot connect to identd on the client" in str(err)
