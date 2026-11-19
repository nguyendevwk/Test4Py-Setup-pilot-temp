import pytest
from sanic.exceptions import URITooLong


def test_default_attributes():
    """URITooLong should expose the correct default status code and quiet flag."""
    exc = URITooLong()
    # Status code is defined on the class
    assert exc.status_code == 414
    # The quiet flag defaults to True as defined in the class
    assert exc.quiet is True
    # No message means the default message from HTTPException is used
    assert exc.message is None
    # No headers, context or extra by default
    assert exc.headers == {}
    assert exc.context == {}
    assert exc.extra == {}


def test_message_and_headers():
    """Providing a custom message and headers should store them correctly."""
    custom_msg = "Custom URI too long error"
    custom_headers = {"X-Custom": "value"}
    exc = URITooLong(custom_msg, headers=custom_headers)
    # The message should be stored as provided
    assert exc.message == custom_msg
    # Headers should be stored exactly as passed
    assert exc.headers == custom_headers
    # Quiet flag remains True unless overridden
    assert exc.quiet is True


def test_context_and_extra():
    """Context and extra data should be preserved and accessible."""
    ctx = {"user_id": 42}
    extra = {"debug": True}
    exc = URITooLong(context=ctx, extra=extra)
    # Context and extra should match the arguments
    assert exc.context == ctx
    assert exc.extra == extra
    # Headers should still be empty by default
    assert exc.headers == {}
