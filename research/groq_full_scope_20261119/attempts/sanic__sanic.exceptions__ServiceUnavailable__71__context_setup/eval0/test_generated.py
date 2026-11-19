import pytest
from sanic.exceptions import ServiceUnavailable
from sanic.helpers import STATUS_CODES


def test_default_service_unavailable_message_and_status():
    """ServiceUnavailable without arguments should use status 503 and default message."""
    exc = ServiceUnavailable()
    assert exc.status_code == 503
    # Default message should be the status description for 503
    expected_msg = STATUS_CODES[503].decode()
    assert exc.args[0] == expected_msg
    # quiet should default to True as defined on the class
    assert exc.quiet is True
    # No custom headers should be present
    assert exc.headers == {}


def test_service_unavailable_with_custom_message_and_headers():
    """Providing a custom message and headers should override defaults."""
    custom_msg = "Service temporarily down"
    custom_headers = {"Retry-After": "120", "X-Custom": "value"}
    exc = ServiceUnavailable(custom_msg, headers=custom_headers)
    assert exc.status_code == 503
    assert exc.args[0] == custom_msg
    # quiet remains True unless overridden
    assert exc.quiet is True
    # Headers should match what was passed
    assert exc.headers == custom_headers


def test_service_unavailable_quiet_flag_and_context():
    """Quiet flag and context should be stored correctly."""
    context = {"detail": "maintenance"}
    exc = ServiceUnavailable(quiet=False, context=context)
    assert exc.status_code == 503
    # Quiet flag overridden to False
    assert exc.quiet is False
    # Context should be stored on the exception
    assert exc.context == context
    # No custom headers
    assert exc.headers == {}
