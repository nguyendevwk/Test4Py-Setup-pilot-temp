import pytest
from sanic.exceptions import URLBuildError
from sanic.helpers import STATUS_CODES


def test_default_message_and_status_code():
    """URLBuildError without arguments should use default status code and message."""
    exc = URLBuildError()
    # status_code should be the class attribute
    assert exc.status_code == 500
    # message should be the default status message for 500
    assert exc.message == STATUS_CODES[500].decode()
    # headers should be empty dict
    assert exc.headers == {}
    # context and extra should be None
    assert exc.context is None
    assert exc.extra is None


def test_custom_message_and_headers():
    """Providing a custom message and headers should override defaults."""
    custom_msg = "Custom error message"
    custom_headers = {"X-Custom": "value"}
    exc = URLBuildError(custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.status_code == 500  # still default status
    assert exc.headers == custom_headers
    # quiet defaults to False
    assert exc.quiet is False
    # context and extra remain None
    assert exc.context is None
    assert exc.extra is None


def test_status_code_and_context():
    """URLBuildError should respect status_code and context when provided."""
    # Use a non-standard status code to ensure message is derived from STATUS_CODES
    exc = URLBuildError(status_code=418, context={"detail": "I'm a teapot"})
    # status_code should be set to 418
    assert exc.status_code == 418
    # message should be derived from STATUS_CODES for 418
    assert exc.message == STATUS_CODES[418].decode()
    # context should be stored
    assert exc.context == {"detail": "I'm a teapot"}
    # extra should be None
    assert exc.extra is None
    # headers should be empty dict
    assert exc.headers == {}
