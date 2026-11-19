import pytest
from youtube_dl.socks import InvalidVersionError

def test_invalid_version_error_message_basic():
    """The error message should contain the expected and got versions in hex."""
    err = InvalidVersionError(0x01, 0x02)
    assert isinstance(err, Exception)
    assert "Expected 01 got 02" in str(err)
    # Ensure the formatting uses two hex digits
    assert "01" in str(err) and "02" in str(err)

def test_invalid_version_error_message_boundary():
    """Test boundary values: 0x00 and 0xFF."""
    err = InvalidVersionError(0x00, 0xFF)
    msg = str(err)
    assert "Expected 00 got ff" in msg.lower()
    # The message should contain both hex values exactly once
    assert msg.lower().count("00") == 1
    assert msg.lower().count("ff") == 1

def test_invalid_version_error_inheritance_and_args():
    """Ensure the error inherits from ProxyError and stores args correctly."""
    err = InvalidVersionError(0x10, 0x20)
    # ProxyError is not imported directly; check that the args tuple contains the code and message
    assert err.args[0] == 0  # code passed to super()
    assert isinstance(err.args[1], str)
    # The message should match the expected format
    expected_msg = "Invalid response version from server. Expected 10 got 20"
    assert err.args[1] == expected_msg
