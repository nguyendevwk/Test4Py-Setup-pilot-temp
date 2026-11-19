import pytest
from sanic.exceptions import PayloadTooLarge


def test_default_payload_too_large_attributes():
    """PayloadTooLarge should have default status_code and quiet flag."""
    exc = PayloadTooLarge()
    # status_code is defined on the class
    assert exc.status_code == 413
    # quiet flag is defined on the class
    assert exc.quiet is True
    # message defaults to None
    assert exc.message is None
    # headers default to None
    assert exc.headers is None
    # context and extra default to None
    assert exc.context is None
    assert exc.extra is None


def test_payload_too_large_with_message_and_headers():
    """Providing a message and custom headers should set the corresponding attributes."""
    custom_message = "Payload exceeds limit"
    custom_headers = {"Retry-After": "120"}
    exc = PayloadTooLarge(message=custom_message, headers=custom_headers)
    assert exc.message == custom_message
    assert exc.headers == custom_headers
    # status_code and quiet remain unchanged
    assert exc.status_code == 413
    assert exc.quiet is True


def test_payload_too_large_str_representation():
    """The string representation of the exception should include the message if provided."""
    exc = PayloadTooLarge(message="Too big")
    # The base HTTPException likely implements __str__ to return the message
    assert str(exc) == "Too big"
    # Without a message, __str__ should return the default status description
    exc_no_msg = PayloadTooLarge()
    # STATUS_CODES is imported in the module; use it to get the default description
    from sanic.helpers import STATUS_CODES
    expected_default = STATUS_CODES.get(exc_no_msg.status_code, "")
    assert str(exc_no_msg) == expected_default
