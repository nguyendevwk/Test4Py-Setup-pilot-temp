import pytest
from sanic.exceptions import ExpectationFailed


def test_default_attributes():
    """Verify that the default status code and quiet flag are set correctly."""
    exc = ExpectationFailed()
    assert exc.status_code == 417
    assert exc.quiet is True
    # The message should be None when not provided
    assert exc.message is None


def test_message_and_headers():
    """Check that a custom message and headers are stored on the exception."""
    custom_msg = "Custom expectation failed"
    custom_headers = {"X-Custom": "value"}
    exc = ExpectationFailed(custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # The status code remains unchanged
    assert exc.status_code == 417


def test_context_and_extra():
    """Ensure that context and extra data are attached correctly."""
    ctx = {"user": "alice", "attempt": 3}
    extra = {"debug": True}
    exc = ExpectationFailed(context=ctx, extra=extra)
    # Context should be accessible via the `context` attribute
    assert exc.context == ctx
    # Extra data should be stored in the `extra` attribute
    assert exc.extra == extra
    # The exception should still have the correct status code
    assert exc.status_code == 417
