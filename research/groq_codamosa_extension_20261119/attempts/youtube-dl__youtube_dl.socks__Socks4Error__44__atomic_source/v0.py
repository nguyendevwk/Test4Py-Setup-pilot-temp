import pytest
from youtube_dl.socks import Socks4Error


def test_socks4_error_attributes():
    """Verify that the error constants are defined correctly."""
    # ERR_SUCCESS should be 90
    assert Socks4Error.ERR_SUCCESS == 90

    # CODES should contain the expected mapping
    expected_codes = {
        91: 'request rejected or failed',
        92: 'request rejected because SOCKS server cannot connect to identd on the client',
        93: 'request rejected because the client program and identd report different user-ids',
    }
    assert Socks4Error.CODES == expected_codes

    # The class should be a subclass of Exception (via ProxyError)
    assert issubclass(Socks4Error, Exception)


def test_socks4_error_lookup_known_code():
    """Lookup of a known error code should return the correct message."""
    code = 92
    message = Socks4Error.CODES[code]
    assert message == 'request rejected because SOCKS server cannot connect to identd on the client'


def test_socks4_error_lookup_unknown_code():
    """Accessing an unknown error code should raise KeyError."""
    with pytest.raises(KeyError):
        _ = Socks4Error.CODES[999]
