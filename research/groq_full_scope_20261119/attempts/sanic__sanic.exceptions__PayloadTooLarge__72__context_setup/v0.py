import pytest
from sanic.exceptions import PayloadTooLarge
from sanic.helpers import STATUS_CODES


def test_payload_too_large_default_message_and_status():
    """When no message is provided, the exception should use the status code
    description from STATUS_CODES and set the status_code to 413."""
    exc = PayloadTooLarge()
    assert exc.status_code == 413
    # STATUS_CODES contains the standard reason phrase for 413
    expected_message = STATUS_CODES[413].decode()
    assert exc.message == expected_message
    # quiet should default to the class attribute
    assert exc.quiet is True
    # headers should be an empty dict by default
    assert exc.headers == {}


def test_payload_too_large_with_custom_message_and_headers():
    """Providing a custom message and headers should override the defaults."""
    custom_msg = "Custom payload too large"
    custom_headers = {"X-Custom": "value"}
    exc = PayloadTooLarge(custom_msg, headers=custom_headers)
    assert exc.status_code == 413
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # quiet remains True unless explicitly overridden
    assert exc.quiet is True


def test_payload_too_large_message_as_integer():
    """Passing a non-string, non-bytes message (e.g., an int) should be accepted
    and stored as-is, without raising an exception."""
    exc = PayloadTooLarge(12345)
    assert exc.status_code == 413
    # The message attribute should be the integer we passed
    assert exc.message == 12345
    # The exception's string representation should match the integer
    assert str(exc) == "12345"
