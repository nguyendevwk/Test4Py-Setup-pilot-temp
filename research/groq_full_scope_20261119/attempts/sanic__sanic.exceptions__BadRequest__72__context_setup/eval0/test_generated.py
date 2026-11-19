import pytest
from sanic.exceptions import BadRequest
from sanic.helpers import STATUS_CODES


def test_default_bad_request_message_and_status():
    """BadRequest without arguments should use default status and message."""
    exc = BadRequest()
    # Status code should be 400 as defined in the class
    assert exc.status_code == 400
    # Default message should be the status text for 400
    expected_msg = STATUS_CODES[400].decode()
    assert exc.args[0] == expected_msg
    # Quiet flag should default to True as set on the class
    assert exc.quiet is True
    # No headers should be present by default
    assert exc.headers == {}


def test_custom_message_and_headers():
    """Providing a custom message and headers should override defaults."""
    custom_msg = "Custom error message"
    custom_headers = {"X-Custom": "value"}
    exc = BadRequest(custom_msg, headers=custom_headers)
    # Message should be the custom string
    assert exc.args[0] == custom_msg
    # Status code remains 400
    assert exc.status_code == 400
    # Headers should include the custom header
    assert exc.headers == custom_headers
    # Quiet flag remains True
    assert exc.quiet is True


def test_context_and_extra_data():
    """Context and extra data should be stored on the exception."""
    context = {"detail": "invalid input"}
    extra = {"debug": "stack trace"}
    exc = BadRequest(context=context, extra=extra)
    # Context should be stored exactly as passed
    assert exc.context == context
    # Extra should be stored exactly as passed
    assert exc.extra == extra
    # Default message should still be the status text
    assert exc.args[0] == STATUS_CODES[400].decode()
    # Headers should be empty by default
    assert exc.headers == {}
