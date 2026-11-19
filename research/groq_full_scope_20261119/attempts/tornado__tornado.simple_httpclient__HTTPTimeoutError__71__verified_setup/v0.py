import pytest
from tornado.simple_httpclient import HTTPTimeoutError
from tornado.httpclient import HTTPError


def test_http_timeout_error_initialization_and_code():
    """Verify that HTTPTimeoutError is a subclass of HTTPError and carries code 599."""
    err = HTTPTimeoutError("test timeout")
    assert isinstance(err, HTTPError)
    assert err.code == 599
    assert err.message == "test timeout"


def test_http_timeout_error_str_returns_message():
    """__str__ should return the message passed to the constructor."""
    err = HTTPTimeoutError("custom message")
    assert str(err) == "custom message"


def test_http_timeout_error_default_message():
    """When no message is provided, __str__ should return the default 'Timeout'."""
    err = HTTPTimeoutError("")
    # The constructor stores an empty string as message; __str__ falls back to "Timeout"
    assert err.message == ""
    assert str(err) == "Timeout"
