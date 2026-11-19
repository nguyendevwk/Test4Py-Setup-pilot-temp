import pytest
from sanic.exceptions import RequestTimeout


def test_default_initialization():
    """RequestTimeout should default to status 408 and quiet True."""
    exc = RequestTimeout()
    assert exc.status_code == 408
    assert exc.quiet is True
    # The default message should be None (no custom message)
    assert exc.message is None
    # No headers by default
    assert exc.headers == {}


def test_custom_message_and_headers():
    """Providing a custom message and headers should set them correctly."""
    custom_msg = "Custom timeout message"
    custom_headers = {"X-Custom-Header": "value"}
    exc = RequestTimeout(message=custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # Status and quiet should remain unchanged
    assert exc.status_code == 408
    assert exc.quiet is True


def test_context_and_extra_are_stored():
    """Context and extra data should be stored on the exception instance."""
    context = {"user_id": 123}
    extra = {"debug_info": "stack trace"}
    exc = RequestTimeout(context=context, extra=extra)
    # Sanic's HTTPException stores context and extra in .context and .extra
    assert getattr(exc, "context", None) == context
    assert getattr(exc, "extra", None) == extra
    # Ensure that these do not affect status or quiet
    assert exc.status_code == 408
    assert exc.quiet is True
