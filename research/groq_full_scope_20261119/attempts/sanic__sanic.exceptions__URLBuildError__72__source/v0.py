import pytest
from sanic.exceptions import URLBuildError
from sanic.exceptions import HTTPException


def test_urlbuilderror_default_status_and_message():
    """URLBuildError should default to status 500 and a default message."""
    exc = URLBuildError()
    assert isinstance(exc, HTTPException)
    assert exc.status_code == 500
    # Default message is None, which should result in a generic message
    assert exc.message is None
    # The default string representation should include the status code
    assert "500" in str(exc)


def test_urlbuilderror_custom_message_and_headers():
    """Custom message and headers should be stored on the exception."""
    custom_msg = "Custom error message"
    custom_headers = {"X-Custom-Header": "value"}
    exc = URLBuildError(message=custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # The string representation should contain the custom message
    assert custom_msg in str(exc)
    # Headers should be accessible via the headers attribute
    assert exc.headers["X-Custom-Header"] == "value"


def test_urlbuilderror_quiet_flag_and_context():
    """The quiet flag should be stored and context should be accessible."""
    context_data = {"detail": "some detail"}
    exc = URLBuildError(quiet=True, context=context_data)
    assert exc.quiet is True
    assert exc.context == context_data
    # The string representation should not include the context dictionary
    assert str(context_data) not in str(exc)
