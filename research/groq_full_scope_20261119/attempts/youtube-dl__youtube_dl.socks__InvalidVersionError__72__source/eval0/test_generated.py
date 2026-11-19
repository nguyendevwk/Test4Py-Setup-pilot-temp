import pytest
from youtube_dl.socks import InvalidVersionError

def test_invalid_version_error_message():
    """The error message should include the expected and got versions in hex."""
    expected = 0x12
    got = 0x34
    err = InvalidVersionError(expected, got)
    assert isinstance(err, Exception)
    # The message should contain the hex representations of both values
    assert f"Expected {expected:02x}" in str(err)
    assert f"got {got:02x}" in str(err)

def test_invalid_version_error_inherits_proxy_error():
    """InvalidVersionError should be a subclass of ProxyError."""
    from youtube_dl.socks import ProxyError
    err = InvalidVersionError(0x01, 0x02)
    assert isinstance(err, ProxyError)

def test_invalid_version_error_code_attribute():
    """The error should expose a code attribute set to 0."""
    err = InvalidVersionError(0x01, 0x02)
    # The base ProxyError constructor is called with code=0
    assert getattr(err, "code", None) == 0
