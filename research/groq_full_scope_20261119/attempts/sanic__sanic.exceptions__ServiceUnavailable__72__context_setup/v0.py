import pytest
from sanic.exceptions import ServiceUnavailable
from sanic.helpers import STATUS_CODES


def test_service_unavailable_default_initialization():
    """ServiceUnavailable should default to status 503 and quiet True."""
    exc = ServiceUnavailable()
    assert isinstance(exc, ServiceUnavailable)
    assert exc.status_code == 503
    assert exc.quiet is True
    # Default message should be the status code description
    expected_msg = STATUS_CODES[503].decode()
    assert exc.args[0] == expected_msg
    # No headers by default
    assert exc.headers == {}


def test_service_unavailable_with_custom_message_and_headers():
    """Providing a custom message and headers should override defaults."""
    custom_msg = "Custom error message"
    custom_headers = {"X-Custom": "value"}
    exc = ServiceUnavailable(custom_msg, headers=custom_headers)
    assert exc.status_code == 503
    assert exc.quiet is True
    assert exc.args[0] == custom_msg
    assert exc.headers == custom_headers
    # Context and extra should be None by default
    assert exc.context is None
    assert exc.extra is None


def test_service_unavailable_bytes_message_and_quiet_flag():
    """Bytes message should be decoded and quiet flag respected."""
    bytes_msg = b"Byte message"
    exc = ServiceUnavailable(bytes_msg, quiet=False)
    assert exc.status_code == 503
    assert exc.quiet is False
    assert exc.args[0] == "Byte message"
    # Ensure headers remain default empty dict
    assert exc.headers == {}
