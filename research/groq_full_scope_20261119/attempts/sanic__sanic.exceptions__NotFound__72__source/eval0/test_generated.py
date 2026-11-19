import pytest
from sanic.exceptions import NotFound
from sanic.helpers import STATUS_CODES


def test_default_message_and_status():
    """Creating a NotFound without a message should use the default status message."""
    exc = NotFound()
    # The default message should be the status code description
    assert exc.message == STATUS_CODES[404]
    # Status code and quiet flag should match the class defaults
    assert exc.status_code == 404
    assert exc.quiet is True
    # No headers should be present by default
    assert exc.headers == {}


def test_custom_message_and_headers():
    """Providing a custom message and headers should override the defaults."""
    custom_msg = "Resource not found"
    custom_headers = {"X-Custom": "value"}
    exc = NotFound(message=custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # Status code remains unchanged
    assert exc.status_code == 404
    # quiet flag remains True
    assert exc.quiet is True


def test_context_and_extra_are_stored():
    """Context and extra data should be stored on the exception instance."""
    context = {"user_id": 42}
    extra = {"debug": True}
    exc = NotFound(context=context, extra=extra)
    # The context and extra attributes should be accessible
    assert exc.context == context
    assert exc.extra == extra
    # They should not affect the message or status code
    assert exc.message == STATUS_CODES[404]
    assert exc.status_code == 404
