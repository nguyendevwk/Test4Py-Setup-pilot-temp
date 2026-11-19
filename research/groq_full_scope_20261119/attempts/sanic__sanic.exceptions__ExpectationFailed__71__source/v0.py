import pytest
from sanic.exceptions import ExpectationFailed
from sanic.helpers import STATUS_CODES


def test_status_code_and_quiet_default():
    """ExpectationFailed should expose the correct status code and default quiet flag."""
    exc = ExpectationFailed()
    assert exc.status_code == 417
    assert exc.quiet is True
    # The default message should be the status description
    assert exc.message == STATUS_CODES[417]


def test_custom_message_and_headers(tmp_path):
    """Providing a custom message and headers should be reflected in the exception."""
    custom_msg = "Custom expectation failed"
    custom_headers = {"X-Custom": "value"}
    exc = ExpectationFailed(custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    # Headers are stored in the `headers` attribute
    assert exc.headers == custom_headers
    # The default status description should not override the custom message
    assert exc.message != STATUS_CODES[417]


def test_context_and_extra_data():
    """Context and extra data should be stored correctly and not interfere with each other."""
    context = {"user": "alice", "attempt": 3}
    extra = {"debug": "info"}
    exc = ExpectationFailed(context=context, extra=extra)
    # Context should be accessible via the `context` attribute
    assert exc.context == context
    # Extra data should be stored separately
    assert exc.extra == extra
    # The message should still be the default status description
    assert exc.message == STATUS_CODES[417]
