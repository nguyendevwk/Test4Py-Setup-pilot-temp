import pytest
from sanic.exceptions import URLBuildError


def test_urlbuilderror_basic_message_and_status():
    """URLBuildError should store the provided message and use the correct status code."""
    err = URLBuildError("Test error message")
    # Status code is defined on the class
    assert err.status_code == 500
    # The message should be accessible via the `message` attribute
    assert getattr(err, "message", None) == "Test error message"
    # The string representation should include the message
    assert "Test error message" in str(err)


def test_urlbuilderror_context_and_extra():
    """URLBuildError should preserve context and extra data passed to it."""
    context = {"key1": "value1", "key2": 2}
    extra = {"secret": "hidden"}
    err = URLBuildError("Context test", context=context, extra=extra)
    # Context and extra should be stored as provided
    assert getattr(err, "context", None) == context
    assert getattr(err, "extra", None) == extra
    # The error message should still be present
    assert err.message == "Context test"
    # The string representation should not expose the extra data
    assert "hidden" not in str(err)


def test_urlbuilderror_headers_and_quiet_flag():
    """URLBuildError should store headers and the quiet flag correctly."""
    headers = {"X-Custom-Header": "value"}
    err = URLBuildError("Header test", quiet=True, headers=headers)
    # Quiet flag should be stored
    assert getattr(err, "quiet", None) is True
    # Headers should be stored
    assert getattr(err, "headers", None) == headers
    # The message should be present
    assert err.message == "Header test"
    # The string representation should include the message but not the headers
    assert "Header test" in str(err)
    assert "X-Custom-Header" not in str(err)
