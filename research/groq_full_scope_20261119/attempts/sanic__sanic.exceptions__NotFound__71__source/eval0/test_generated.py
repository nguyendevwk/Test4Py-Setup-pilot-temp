import pytest
from sanic.exceptions import NotFound
from sanic.helpers import STATUS_CODES


def test_default_notfound_attributes():
    """Verify default attributes of NotFound."""
    exc = NotFound()
    # status code should be 404
    assert exc.status_code == 404
    # quiet flag should be True by default
    assert exc.quiet is True
    # default message should be None, leading to status message
    assert exc.message is None
    # The default string representation should use the status message
    expected_msg = STATUS_CODES[404]
    assert str(exc) == expected_msg


def test_notfound_with_custom_message_and_headers():
    """Verify custom message and headers are stored correctly."""
    custom_msg = "Resource missing"
    custom_headers = {"X-Custom": "value"}
    exc = NotFound(message=custom_msg, headers=custom_headers)
    # message should be set to the custom string
    assert exc.message == custom_msg
    # headers should be accessible via the headers attribute
    assert exc.headers == custom_headers
    # string representation should use the custom message
    assert str(exc) == custom_msg


def test_notfound_inherits_http_exception_behavior():
    """Ensure NotFound behaves like an HTTPException regarding context."""
    context = {"detail": "Not found in DB"}
    exc = NotFound(context=context)
    # context should be stored in the exception
    assert exc.context == context
    # The exception should be instance of HTTPException (via NotFound)
    from sanic.exceptions import HTTPException
    assert isinstance(exc, HTTPException)
