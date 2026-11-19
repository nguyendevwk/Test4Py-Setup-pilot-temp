import pytest
from sanic.exceptions import ServiceUnavailable
from sanic.helpers import STATUS_CODES


def test_service_unavailable_default_behavior():
    """Verify default attributes and message handling."""
    exc = ServiceUnavailable()
    # Default status code and quiet flag
    assert exc.status_code == 503
    assert exc.quiet is True
    # Default message should be the status description
    assert exc.message == STATUS_CODES[503]
    # No context or headers by default
    assert exc.context == {}
    assert exc.headers == {}


def test_service_unavailable_with_custom_message_and_headers():
    """Verify custom message, context, and headers are stored correctly."""
    custom_msg = "Service temporarily down"
    custom_context = {"reason": "maintenance"}
    custom_headers = {"Retry-After": "120"}
    exc = ServiceUnavailable(
        message=custom_msg,
        context=custom_context,
        headers=custom_headers,
    )
    # Custom message should override default
    assert exc.message == custom_msg
    # Context and headers should be preserved
    assert exc.context == custom_context
    assert exc.headers == custom_headers
    # Status code remains unchanged
    assert exc.status_code == 503


def test_service_unavailable_bytes_message_and_error_on_invalid_headers():
    """Verify bytes message handling and that invalid headers raise TypeError."""
    # Bytes message should be decoded to str
    exc = ServiceUnavailable(message=b"Binary message")
    assert exc.message == "Binary message"

    # Headers must be a mapping; passing a list should raise TypeError
    with pytest.raises(TypeError):
        ServiceUnavailable(headers=[("Retry-After", "120")])
