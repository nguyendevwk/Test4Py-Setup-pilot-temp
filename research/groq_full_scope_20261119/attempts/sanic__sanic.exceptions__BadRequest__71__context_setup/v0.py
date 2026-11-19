import pytest
from sanic.exceptions import BadRequest
from sanic.helpers import STATUS_CODES


def test_default_bad_request_message_and_status():
    """BadRequest with no arguments should use default status and message."""
    exc = BadRequest()
    # Status code should be 400 as defined on the class
    assert exc.status_code == 400
    # Default message should be the status text for 400
    expected_msg = STATUS_CODES[400].decode()
    assert exc.args[0] == expected_msg
    # quiet flag should default to True as set on the class
    assert exc.quiet is True
    # No headers should be present by default
    assert exc.headers == {}


def test_custom_message_and_headers():
    """Providing a custom message and headers should override defaults."""
    custom_msg = "Custom error message"
    custom_headers = {"X-Custom": "value"}
    exc = BadRequest(custom_msg, headers=custom_headers)
    # Status code remains 400
    assert exc.status_code == 400
    # Message should be the custom string
    assert exc.args[0] == custom_msg
    # Headers should include the custom header
    assert exc.headers == custom_headers
    # quiet flag remains True
    assert exc.quiet is True


def test_message_as_bytes_and_context():
    """Message can be provided as bytes and context should be stored."""
    byte_msg = b"Byte message"
    context = {"detail": "extra info"}
    exc = BadRequest(byte_msg, context=context)
    # Message should be decoded to string
    assert exc.args[0] == "Byte message"
    # Context should be stored on the exception
    assert exc.context == context
    # Status code and quiet flag default correctly
    assert exc.status_code == 400
    assert exc.quiet is True
