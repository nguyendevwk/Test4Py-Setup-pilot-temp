import pytest
from sanic.exceptions import PayloadTooLarge


def test_payload_too_large_default_attributes():
    """PayloadTooLarge should expose the correct default status and quiet flag."""
    exc = PayloadTooLarge()
    # status_code is defined on the class
    assert exc.status_code == 413
    # quiet flag is set to True by default
    assert exc.quiet is True
    # message defaults to None
    assert exc.message is None
    # headers, context, and extra should be empty dicts if not provided
    assert exc.headers == {}
    assert exc.context == {}
    assert exc.extra == {}


def test_payload_too_large_with_custom_message_and_headers():
    """Providing a custom message and headers should store them correctly."""
    custom_msg = "Payload exceeds limit"
    custom_headers = {"Retry-After": "120", "X-Custom": "value"}
    exc = PayloadTooLarge(custom_msg, headers=custom_headers)
    # message should be stored as provided
    assert exc.message == custom_msg
    # headers should reflect the custom dict
    assert exc.headers == custom_headers
    # quiet flag remains True unless explicitly overridden
    assert exc.quiet is True
    # context and extra remain empty
    assert exc.context == {}
    assert exc.extra == {}


def test_payload_too_large_context_and_extra():
    """Context and extra mappings should be stored and accessible."""
    ctx = {"user_id": 42, "attempt": 3}
    extra = {"debug": True}
    exc = PayloadTooLarge(context=ctx, extra=extra)
    # context and extra should match the provided dictionaries
    assert exc.context == ctx
    assert exc.extra == extra
    # message defaults to None
    assert exc.message is None
    # headers default to empty dict
    assert exc.headers == {}
