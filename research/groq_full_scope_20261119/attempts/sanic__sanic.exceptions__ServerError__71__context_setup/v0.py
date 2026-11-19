import pytest
from sanic.exceptions import ServerError
from sanic.helpers import STATUS_CODES


def test_default_server_error_message_and_status():
    """ServerError with no arguments should use default status and message."""
    err = ServerError()
    # status_code should be 500 as defined on the class
    assert err.status_code == 500
    # message should be the default status message for 500
    expected_msg = STATUS_CODES.get(500, b"").decode()
    assert err.message == expected_msg
    # headers should be empty dict by default
    assert err.headers == {}


def test_server_error_with_custom_message_and_headers():
    """ServerError should correctly store a custom message and headers."""
    custom_msg = "Custom error occurred"
    custom_headers = {"X-Custom": "value"}
    err = ServerError(custom_msg, headers=custom_headers)
    assert err.status_code == 500
    assert err.message == custom_msg
    assert err.headers == custom_headers
    # Ensure that the message is not overridden by status code
    assert err.message != STATUS_CODES.get(500, b"").decode()


def test_server_error_quiet_and_context():
    """ServerError should preserve quiet flag and context mapping."""
    context = {"detail": "Something went wrong"}
    err = ServerError(quiet=True, context=context)
    assert err.quiet is True
    assert err.context == context
    # The message should still be the default status message
    assert err.message == STATUS_CODES.get(500, b"").decode()
