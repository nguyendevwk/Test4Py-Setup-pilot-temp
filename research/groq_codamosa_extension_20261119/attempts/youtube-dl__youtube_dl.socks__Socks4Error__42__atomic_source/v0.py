import pytest
from youtube_dl.socks import Socks4Error

def test_err_success_value():
    """Socks4Error should expose the correct success code."""
    assert Socks4Error.ERR_SUCCESS == 90

def test_codes_mapping():
    """The CODES dictionary should contain the expected error messages."""
    expected = {
        91: 'request rejected or failed',
        92: 'request rejected because SOCKS server cannot connect to identd on the client',
        93: 'request rejected because the client program and identd report different user-ids'
    }
    assert Socks4Error.CODES == expected
    # Ensure all keys are integers and values are strings
    for key, value in Socks4Error.CODES.items():
        assert isinstance(key, int)
        assert isinstance(value, str)

def test_exception_inheritance():
    """Socks4Error should be an exception type and inherit from Exception."""
    # Instantiate with a message
    exc = Socks4Error("test message")
    # It should be an instance of Exception
    assert isinstance(exc, Exception)
    # The message should be stored correctly
    assert str(exc) == "test message"
