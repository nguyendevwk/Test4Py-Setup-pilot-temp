import pytest
from sanic.exceptions import HTTPException
from sanic.helpers import STATUS_CODES


def test_http_exception_with_string_message_and_custom_headers():
    """Verify that a string message is stored correctly and custom headers are applied."""
    exc = HTTPException(
        "Custom error",
        quiet=True,
        context={"detail": "test"},
        extra={"internal": "debug"},
        headers={"X-Custom": "value"},
    )
    # The message should be the string passed
    assert exc.args[0] == "Custom error"
    assert exc.message == "Custom error"
    # Status code defaults to the class attribute (500)
    assert exc.status_code == 500
    # Quiet flag should be set
    assert exc.quiet is True
    # Headers should contain the custom header
    assert exc.headers == {"X-Custom": "value"}
    # Context and extra should be stored as provided
    assert exc.context == {"detail": "test"}
    assert exc.extra == {"internal": "debug"}


def test_http_exception_with_bytes_message_and_default_headers():
    """Verify that a bytes message is decoded and default headers are used."""
    msg_bytes = b"Byte error"
    exc = HTTPException(msg_bytes)
    # The message should be decoded to a string
    assert exc.args[0] == "Byte error"
    assert exc.message == "Byte error"
    # Default headers should be an empty dict
    assert exc.headers == {}
    # Status code defaults to 500
    assert exc.status_code == 500
    # Quiet flag defaults to the class attribute (False)
    assert exc.quiet is False


def test_http_exception_with_missing_message_and_status_code_lookup():
    """Verify that when no message is provided, the status code message is used."""
    # Create a subclass with a specific status code
    class NotFound(HTTPException):
        status_code = 404

    exc = NotFound()
    # The message should be the standard status message for 404
    expected_msg = STATUS_CODES.get(404, b"").decode()
    assert exc.args[0] == expected_msg
    assert exc.message == expected_msg
    # Status code should be the subclass's status_code
    assert exc.status_code == 404
