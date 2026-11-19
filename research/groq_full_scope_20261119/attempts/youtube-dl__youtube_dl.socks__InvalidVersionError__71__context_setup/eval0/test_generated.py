import pytest
from youtube_dl.socks import InvalidVersionError, ProxyError


def test_invalid_version_error_message_and_inheritance():
    """Verify that InvalidVersionError formats its message correctly and inherits from ProxyError."""
    expected = 0x01
    got = 0x02
    exc = InvalidVersionError(expected, got)
    # The message should contain the hex representations of the versions
    assert f"Expected {expected:02x}" in str(exc)
    assert f"got {got:02x}" in str(exc)
    # It should be an instance of ProxyError
    assert isinstance(exc, ProxyError)
    # The error code should be 0 as passed to ProxyError
    assert exc.args[0] == 0


def test_invalid_version_error_with_same_versions():
    """When the expected and got versions are the same, the message should reflect that."""
    version = 0x0a
    exc = InvalidVersionError(version, version)
    assert f"Expected {version:02x}" in str(exc)
    assert f"got {version:02x}" in str(exc)
    # No exception should be raised during initialization
    assert isinstance(exc, ProxyError)


def test_invalid_version_error_invalid_input_types():
    """Passing non-integer types should raise a TypeError during formatting."""
    with pytest.raises(TypeError):
        InvalidVersionError("not-an-int", 0x01)
    with pytest.raises(TypeError):
        InvalidVersionError(0x01, None)
