import pytest
from youtube_dl.socks import Socks4Error


def test_socks4error_constants():
    """Verify that the class constants are defined correctly."""
    # ERR_SUCCESS should be 90
    assert Socks4Error.ERR_SUCCESS == 90

    # CODES should contain the expected mapping
    expected_codes = {
        91: 'request rejected or failed',
        92: 'request rejected because SOCKS server cannot connect to identd on the client',
        93: 'request rejected because the client program and identd report different user-ids'
    }
    assert isinstance(Socks4Error.CODES, dict)
    assert Socks4Error.CODES == expected_codes


def test_socks4error_instantiation_and_message():
    """Ensure that Socks4Error can be instantiated and behaves like an exception."""
    # Instantiate with a custom message
    msg = "Custom error message"
    exc = Socks4Error(msg)

    # The exception should be an instance of Socks4Error and its base ProxyError
    assert isinstance(exc, Socks4Error)
    # The message should be stored in the exception args
    assert exc.args == (msg,)

    # Raising and catching the exception should preserve the message
    with pytest.raises(Socks4Error) as excinfo:
        raise exc
    assert str(excinfo.value) == msg


def test_socks4error_codes_access_and_error():
    """Test accessing known and unknown codes in the CODES dictionary."""
    # Known code should return the correct description
    assert Socks4Error.CODES[91] == 'request rejected or failed'
    assert Socks4Error.CODES[92] == 'request rejected because SOCKS server cannot connect to identd on the client'
    assert Socks4Error.CODES[93] == 'request rejected because the client program and identd report different user-ids'

    # Accessing an unknown code should raise KeyError
    with pytest.raises(KeyError):
        _ = Socks4Error.CODES[99]
