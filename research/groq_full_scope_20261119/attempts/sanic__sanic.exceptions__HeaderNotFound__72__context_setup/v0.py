import pytest
from sanic.exceptions import HeaderNotFound


def test_header_not_found_default_status_and_quiet():
    """HeaderNotFound should default to status 400 and quiet True."""
    exc = HeaderNotFound()
    assert isinstance(exc, HeaderNotFound)
    assert exc.status_code == 400
    # quiet defaults to True as defined in BadRequest
    assert exc.quiet is True
    # No message means default message from HTTPException
    assert exc.message is None


def test_header_not_found_custom_message_and_headers():
    """Providing a custom message and headers should reflect in the exception."""
    custom_msg = "Missing required header"
    custom_headers = {"X-Custom-Error": "true"}
    exc = HeaderNotFound(custom_msg, headers=custom_headers)
    assert exc.message == custom_msg
    assert exc.headers == custom_headers
    # quiet remains default True unless overridden
    assert exc.quiet is True


def test_header_not_found_quiet_false_and_context():
    """Setting quiet to False and providing context should store them correctly."""
    context = {"header": "X-Auth-Token"}
    exc = HeaderNotFound(quiet=False, context=context)
    assert exc.quiet is False
    assert exc.context == context
    # status_code remains 400
    assert exc.status_code == 400
