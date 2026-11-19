import pytest
from sanic.exceptions import URLBuildError


def test_default_initialization():
    """URLBuildError with no arguments should have status_code 500 and no message."""
    err = URLBuildError()
    assert isinstance(err, URLBuildError)
    assert err.status_code == 500
    # The default message is None, which should be represented as None in the instance
    assert err.message is None
    # quiet, context, extra, headers should all be None by default
    assert err.quiet is None
    assert err.context is None
    assert err.extra is None
    assert err.headers is None


def test_message_and_bytes_handling():
    """URLBuildError should store string and bytes messages correctly."""
    msg_str = "A string message"
    msg_bytes = b"Binary message"
    err_str = URLBuildError(msg_str)
    err_bytes = URLBuildError(msg_bytes)
    # String message is stored as is
    assert err_str.message == msg_str
    # Bytes message is stored as is
    assert err_bytes.message == msg_bytes
    # Both errors should still have status_code 500
    assert err_str.status_code == 500
    assert err_bytes.status_code == 500


def test_context_extra_and_headers():
    """URLBuildError should correctly store context, extra, and headers."""
    context = {"key1": "value1"}
    extra = {"debug": True}
    headers = {"X-Custom": "Test"}
    err = URLBuildError(
        "Error with context",
        context=context,
        extra=extra,
        headers=headers,
    )
    assert err.message == "Error with context"
    assert err.context == context
    assert err.extra == extra
    assert err.headers == headers
    # Ensure that modifying the original dicts does not affect the stored ones
    context["key1"] = "changed"
    extra["debug"] = False
    headers["X-Custom"] = "Modified"
    assert err.context["key1"] == "value1"
    assert err.extra["debug"] is True
    assert err.headers["X-Custom"] == "Test"
