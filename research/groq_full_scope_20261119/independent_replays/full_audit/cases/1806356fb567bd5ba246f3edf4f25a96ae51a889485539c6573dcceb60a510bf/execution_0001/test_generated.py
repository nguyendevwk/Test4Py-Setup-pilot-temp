import pytest
from youtube_dl.socks import InvalidVersionError, ProxyError

def test_invalid_version_error_message_and_code():
    """Verify that the error message contains the expected hex values and the code is set to 0."""
    expected = 0x01
    got = 0x02
    err = InvalidVersionError(expected, got)
    assert isinstance(err, ProxyError)
    assert err.args[0] == 0  # code
    assert f"Expected {expected:02x}" in err.args[1]
    assert f"got {got:02x}" in err.args[1]

def test_invalid_version_error_with_zero_values():
    """Test the edge case where both expected and got versions are zero."""
    err = InvalidVersionError(0x00, 0x00)
    assert err.args[0] == 0
    assert err.args[1] == "Invalid response version from server. Expected 00 got 00"

def test_invalid_version_error_with_max_byte_values():
    """Test the maximum byte values (0xFF) for expected and got."""
    err = InvalidVersionError(0xFF, 0xFF)
    assert err.args[0] == 0
    assert err.args[1] == "Invalid response version from server. Expected ff got ff"
