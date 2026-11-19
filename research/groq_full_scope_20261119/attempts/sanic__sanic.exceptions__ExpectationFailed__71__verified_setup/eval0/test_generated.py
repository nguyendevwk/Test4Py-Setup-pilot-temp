import pytest
from sanic.exceptions import ExpectationFailed
from sanic.helpers import STATUS_CODES


def test_default_status_and_quiet():
    """ExpectationFailed should default to status 417 and quiet=True."""
    exc = ExpectationFailed()
    assert exc.status_code == 417
    assert exc.quiet is True
    # The default message should be the status description
    assert exc.message == STATUS_CODES[417]


def test_custom_message_and_headers():
    """Custom message and headers should be stored correctly."""
    custom_msg = "Custom expectation failed"
    custom_headers = {"X-Custom": "value"}
    exc = ExpectationFailed(custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # The status code remains unchanged
    assert exc.status_code == 417


def test_context_and_extra_data():
    """Context and extra data should be accessible via the exception."""
    ctx = {"user": "alice", "attempt": 3}
    extra = {"debug": True}
    exc = ExpectationFailed(context=ctx, extra=extra)
    # Context is stored on the exception
    assert exc.context == ctx
    # Extra data is stored but not exposed in the public API
    assert getattr(exc, "extra", None) == extra
