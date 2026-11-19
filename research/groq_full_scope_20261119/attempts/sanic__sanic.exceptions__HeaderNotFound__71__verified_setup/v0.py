import pytest
from sanic.exceptions import HeaderNotFound

def test_header_not_found_default_status_and_message():
    """HeaderNotFound should default to status 400 and a default message."""
    exc = HeaderNotFound()
    # Status code should be 400
    assert exc.status == 400
    # Default message should be the standard HTTP reason phrase
    assert exc.message == "Bad Request"

def test_header_not_found_with_bytes_message_and_headers():
    """HeaderNotFound should accept a bytes message and custom headers."""
    custom_headers = {"X-Custom-Header": "value"}
    exc = HeaderNotFound(b"Custom error", headers=custom_headers)
    # Message should be preserved as bytes
    assert isinstance(exc.message, bytes)
    assert exc.message == b"Custom error"
    # Headers should be stored and accessible
    assert exc.headers == custom_headers

def test_header_not_found_context_and_extra_storage():
    """HeaderNotFound should store context and extra data correctly."""
    context = {"user_id": 123}
    extra = {"debug": True}
    exc = HeaderNotFound(context=context, extra=extra)
    # Context and extra should be stored as provided
    assert exc.context == context
    assert exc.extra == extra
