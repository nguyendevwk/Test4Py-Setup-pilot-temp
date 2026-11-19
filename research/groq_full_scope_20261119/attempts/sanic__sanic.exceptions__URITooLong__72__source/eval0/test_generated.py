import pytest
from sanic.exceptions import URITooLong


def test_default_uri_too_long_initialization():
    """URITooLong should default to status 414 and quiet True."""
    exc = URITooLong()
    assert isinstance(exc, URITooLong)
    assert exc.status_code == 414
    assert exc.quiet is True
    # Default message should be the status phrase
    assert exc.message == "URI Too Long"
    # No custom headers or context
    assert exc.headers == {}
    assert exc.context == {}
    assert exc.extra == {}


def test_uri_too_long_with_custom_message_and_context():
    """Custom message and context should be preserved."""
    custom_msg = "Custom error message"
    context = {"detail": "URI exceeded limit"}
    exc = URITooLong(message=custom_msg, context=context)
    assert exc.message == custom_msg
    assert exc.context == context
    # Context should not affect headers or extra
    assert exc.headers == {}
    assert exc.extra == {}


def test_uri_too_long_with_headers_and_extra():
    """Headers and extra data should be stored correctly."""
    headers = {"Retry-After": "120"}
    extra = {"debug": "stacktrace"}
    exc = URITooLong(headers=headers, extra=extra)
    assert exc.headers == headers
    assert exc.extra == extra
    # Ensure quiet remains True
    assert exc.quiet is True
