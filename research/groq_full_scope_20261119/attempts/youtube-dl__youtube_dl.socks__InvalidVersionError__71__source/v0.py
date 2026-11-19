import pytest
from youtube_dl.socks import InvalidVersionError


def test_invalid_version_error_message():
    """The error message should include the expected and received
    version numbers formatted as two‑digit hex values."""
    expected = 0x12
    got = 0x34
    err = InvalidVersionError(expected, got)
    assert isinstance(err, Exception)
    assert err.args[0] == 0  # code passed to ProxyError
    expected_msg = f"Invalid response version from server. Expected {expected:02x} got {got:02x}"
    assert err.args[1] == expected_msg
    assert str(err) == expected_msg


def test_invalid_version_error_inherits_from_proxy_error():
    """InvalidVersionError should be a subclass of ProxyError."""
    from youtube_dl.socks import ProxyError
    err = InvalidVersionError(0x01, 0x02)
    assert isinstance(err, ProxyError)
    assert issubclass(InvalidVersionError, ProxyError)


def test_invalid_version_error_code_attribute():
    """The error code passed to the base class should be stored in the
    first argument of the exception."""
    err = InvalidVersionError(0x0a, 0x0b)
    # ProxyError likely stores the code in args[0]
    assert err.args[0] == 0
    # The code is not exposed as a separate attribute, but the args tuple
    # contains the code as the first element.
    assert isinstance(err.args[0], int)
