import pytest
from youtube_dl.socks import InvalidVersionError

def test_invalid_version_error_message_basic():
    """Check that the error message contains the expected hex values."""
    err = InvalidVersionError(0x01, 0x02)
    assert isinstance(err, Exception)
    assert "Expected 01 got 02" in str(err)
    # The message should not contain the raw integer values
    assert "1" not in str(err) or "2" not in str(err)

def test_invalid_version_error_message_boundary():
    """Test boundary values 0x00 and 0xFF."""
    err = InvalidVersionError(0x00, 0xFF)
    msg = str(err)
    assert "Expected 00 got ff" in msg
    # Ensure the hex representation is lower case for the got value
    assert msg.endswith("got ff") or msg.endswith("got ff")

def test_invalid_version_error_type_and_args():
    """Ensure the error is of the correct type and stores args correctly."""
    err = InvalidVersionError(0x10, 0x20)
    # The args tuple should contain the error code and the message
    assert err.args[0] == 0  # error code passed to ProxyError
    assert isinstance(err.args[1], str)
    # The message should be exactly as formatted
    expected_msg = "Invalid response version from server. Expected 10 got 20"
    assert err.args[1] == expected_msg
