import pytest
from sanic.exceptions import PayloadTooLarge

def test_default_payload_too_large_initialization():
    """PayloadTooLarge should default to status 413 and quiet True."""
    exc = PayloadTooLarge()
    assert exc.status_code == 413
    assert exc.quiet is True
    # Default message should be None, which results in a generic 413 response
    assert exc.message is None
    # No headers by default
    assert exc.headers == {}

def test_payload_too_large_with_custom_message_and_headers():
    """Custom message and headers should be preserved in the exception."""
    custom_msg = "File size exceeds limit"
    custom_headers = {"X-Custom-Header": "value"}
    exc = PayloadTooLarge(custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # Quiet should still be True unless explicitly overridden
    assert exc.quiet is True

def test_payload_too_large_quiet_flag_can_be_overridden():
    """Quiet flag can be set to False when constructing the exception."""
    exc = PayloadTooLarge(quiet=False)
    assert exc.quiet is False
    # Ensure status code remains unchanged
    assert exc.status_code == 413
