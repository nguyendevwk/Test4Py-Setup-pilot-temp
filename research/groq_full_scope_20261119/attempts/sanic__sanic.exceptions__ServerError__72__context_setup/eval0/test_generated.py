import pytest
from sanic.exceptions import ServerError
from sanic.helpers import STATUS_CODES


def test_default_server_error_message_and_status():
    """ServerError without arguments should use default status and message."""
    err = ServerError()
    # status_code should be 500 as defined on the class
    assert err.status_code == 500
    # message should be the default status message for 500
    expected_msg = STATUS_CODES.get(500, b"").decode()
    assert err.message == expected_msg
    # headers should be empty dict by default
    assert err.headers == {}


def test_server_error_with_custom_message_and_headers():
    """ServerError should accept a custom message and headers."""
    custom_msg = "Custom server error occurred"
    custom_headers = {"X-Custom": "value", "Content-Type": "text/plain"}
    err = ServerError(custom_msg, headers=custom_headers)
    # message should be the custom string
    assert err.message == custom_msg
    # status_code remains 500
    assert err.status_code == 500
    # headers should match what was passed
    assert err.headers == custom_headers
    # quiet should default to False
    assert err.quiet is False


def test_server_error_context_and_extra():
    """ServerError should store context and extra data correctly."""
    context_data = {"detail": "Something went wrong", "code": 123}
    extra_data = {"internal": "debug info"}
    err = ServerError("Error", context=context_data, extra=extra_data)
    # context and extra should be stored as provided
    assert err.context == context_data
    assert err.extra == extra_data
    # message should be the provided string
    assert err.message == "Error"
    # status_code remains 500
    assert err.status_code == 500
