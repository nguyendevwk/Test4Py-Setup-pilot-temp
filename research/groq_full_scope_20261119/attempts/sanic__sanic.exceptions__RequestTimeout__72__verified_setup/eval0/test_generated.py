import pytest
from sanic.exceptions import RequestTimeout


def test_default_initialization():
    """RequestTimeout should default to status 408 and quiet=True."""
    exc = RequestTimeout()
    assert exc.status_code == 408
    assert exc.quiet is True
    # Default message should be None, which results in default status message
    assert exc.message is None
    # No headers by default
    assert exc.headers == {}


def test_custom_message_and_headers():
    """Providing a custom message and headers should set them correctly."""
    custom_msg = "Custom timeout message"
    custom_headers = {"Retry-After": "120", "X-Custom": "value"}
    exc = RequestTimeout(custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    # Headers should be exactly as provided
    assert exc.headers == custom_headers
    # quiet should remain True unless explicitly overridden
    assert exc.quiet is True


def test_bytes_message_and_quiet_flag():
    """Bytes message should be accepted and quiet flag should be respected."""
    byte_msg = b"Byte message"
    exc = RequestTimeout(byte_msg, quiet=False)
    assert exc.message == byte_msg
    # quiet flag should override default
    assert exc.quiet is False
    # Ensure headers remain empty
    assert exc.headers == {}
