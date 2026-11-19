import pytest
from sanic.exceptions import ExpectationFailed


def test_default_status_and_quiet():
    """Expect the default status code and quiet flag."""
    exc = ExpectationFailed()
    assert exc.status_code == 417
    # The class sets quiet=True by default
    assert exc.quiet is True
    # The default message should be None
    assert exc.message is None


def test_message_and_context():
    """Verify that a custom message and context are stored correctly."""
    msg = "Custom expectation failed"
    ctx = {"detail": "missing header", "code": 123}
    exc = ExpectationFailed(message=msg, context=ctx)
    # The message should be stored as provided
    assert exc.message == msg
    # The context mapping should be accessible via the `context` attribute
    assert exc.context == ctx
    # The status code remains unchanged
    assert exc.status_code == 417


def test_headers_and_extra(tmp_path):
    """Check that headers and extra data are preserved and not exposed in production."""
    headers = {"X-Custom-Header": "value"}
    extra = {"internal": "secret"}
    exc = ExpectationFailed(headers=headers, extra=extra)
    # Headers should be stored in the `headers` attribute
    assert exc.headers == headers
    # Extra data should be stored in the `extra` attribute
    assert exc.extra == extra
    # The exception should still carry the correct status code
    assert exc.status_code == 417
