import pytest
from youtube_dl.socks import Socks4Error


def test_socks4error_initialization_and_attributes():
    """Socks4Error should store the provided code and message."""
    err = Socks4Error(code=91, msg="Test message")
    assert err.code == 91
    assert err.msg == "Test message"
    # The base ProxyError (not shown) likely stores these as attributes
    assert hasattr(err, "code") and hasattr(err, "msg")


def test_socks4error_known_codes_mapping():
    """The CODES mapping should contain expected error descriptions."""
    # Known codes from the class definition
    for code, description in Socks4Error.CODES.items():
        assert isinstance(code, int)
        assert isinstance(description, str)
        # Ensure that the description matches the expected string
        if code == 91:
            assert description == "request rejected or failed"
        elif code == 92:
            assert description == "request rejected because SOCKS server cannot connect to identd on the client"
        elif code == 93:
            assert description == "request rejected because the client program and identd report different user-ids"
    # ERR_SUCCESS should be defined and equal to 90
    assert Socks4Error.ERR_SUCCESS == 90


def test_socks4error_str_representation():
    """The string representation should include the code and message."""
    err = Socks4Error(code=92, msg="Connection failed")
    # The default __str__ of Exception includes the message; we check that
    # the code is also present in the string representation if the class
    # implements it accordingly.
    representation = str(err)
    assert "Connection failed" in representation
    assert "92" in representation
    # Ensure that the representation is not empty
    assert representation.strip() != ""
