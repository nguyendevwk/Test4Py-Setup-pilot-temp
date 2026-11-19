import pytest
from sanic.exceptions import URITooLong
from sanic.helpers import STATUS_CODES


def test_default_message_and_status_code():
    """URITooLong without arguments should use default status code and message."""
    exc = URITooLong()
    # Status code should be 414
    assert exc.status_code == 414
    # Default message should be the status description
    expected_msg = STATUS_CODES[414].decode()
    assert exc.args[0] == expected_msg
    # Quiet flag should be True as defined on the class
    assert exc.quiet is True
    # No headers by default
    assert exc.headers == {}


def test_custom_message_and_headers():
    """Providing a custom message and headers should override defaults."""
    custom_msg = "Custom URI too long error"
    custom_headers = {"X-Custom": "value"}
    exc = URITooLong(custom_msg, headers=custom_headers)
    # Status code remains 414
    assert exc.status_code == 414
    # Message should be the custom one
    assert exc.args[0] == custom_msg
    # Headers should include the custom header
    assert exc.headers == custom_headers
    # Quiet flag remains True
    assert exc.quiet is True


def test_status_code_and_quiet_override():
    """Explicitly overriding status_code and quiet should work."""
    # Use a different status code to see that it is respected
    exc = URITooLong(status_code=400, quiet=False)
    # Status code should be overridden to 400
    assert exc.status_code == 400
    # Quiet flag should be overridden to False
    assert exc.quiet is False
    # Message should be the default for 400
    expected_msg = STATUS_CODES[400].decode()
    assert exc.args[0] == expected_msg
