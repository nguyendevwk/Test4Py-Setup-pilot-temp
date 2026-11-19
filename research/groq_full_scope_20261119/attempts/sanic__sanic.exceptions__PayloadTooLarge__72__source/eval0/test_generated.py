import pytest
from sanic.exceptions import PayloadTooLarge
from sanic.helpers import STATUS_CODES


def test_payload_too_large_default_attributes():
    """Verify default status code, quiet flag and default message handling."""
    exc = PayloadTooLarge()
    # Status code should match the HTTP 413 code
    assert exc.status_code == 413
    # Quiet flag should be True by default
    assert exc.quiet is True
    # Default message should be None, resulting in the generic status text
    assert exc.message is None
    # The default string representation should use the status text
    assert str(exc) == STATUS_CODES[413]


def test_payload_too_large_custom_message_and_headers():
    """Ensure custom message and headers are stored correctly."""
    custom_msg = "File too large"
    custom_headers = {"X-Custom-Header": "value"}
    exc = PayloadTooLarge(message=custom_msg, headers=custom_headers)
    # The message should be preserved
    assert exc.message == custom_msg
    # Headers should be accessible via the headers attribute
    assert exc.headers == custom_headers
    # The string representation should include the custom message
    assert str(exc) == custom_msg


def test_payload_too_large_context_and_extra():
    """Check that context and extra data are stored and not exposed in the client response."""
    context = {"user_id": 42}
    extra = {"internal_id": "abc123"}
    exc = PayloadTooLarge(context=context, extra=extra)
    # Context should be stored in the exception
    assert exc.context == context
    # Extra should be stored but not part of the client-facing data
    assert exc.extra == extra
    # The client-facing data should not contain the 'internal_id' key
    client_data = exc.to_dict()
    assert "internal_id" not in client_data
    assert client_data.get("user_id") == 42
