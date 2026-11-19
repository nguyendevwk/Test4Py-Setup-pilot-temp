import pytest
from youtube_dl.socks import Socks4Error, ProxyError


def test_socks4_error_constants():
    """Socks4Error should expose the correct constants."""
    # ERR_SUCCESS should be 90
    assert Socks4Error.ERR_SUCCESS == 90

    # CODES should be a mapping with expected keys and values
    expected = {
        91: 'request rejected or failed',
        92: 'request rejected because SOCKS server cannot connect to identd on the client',
        93: 'request rejected because the client program and identd report different user-ids'
    }
    assert isinstance(Socks4Error.CODES, dict)
    assert Socks4Error.CODES == expected


def test_socks4_error_inheritance():
    """Socks4Error must inherit from ProxyError."""
    # Instantiate with a known code to ensure it can be created
    err = Socks4Error(91)
    # The instance should be a ProxyError
    assert isinstance(err, ProxyError)
    # The error message should correspond to the code mapping
    assert str(err) == Socks4Error.CODES[91]


def test_socks4_error_code_lookup():
    """Lookup of unknown codes should raise KeyError."""
    # Known code should return a string
    assert Socks4Error.CODES[92] == 'request rejected because SOCKS server cannot connect to identd on the client'

    # Unknown code should raise KeyError
    with pytest.raises(KeyError):
        _ = Socks4Error.CODES[999]
