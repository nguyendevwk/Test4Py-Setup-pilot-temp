import pytest
from tornado.httpclient import HTTPError
from tornado.simple_httpclient import HTTPStreamClosedError


def test_httpstreamclosederror_inherits_httperror_and_sets_code():
    """HTTPStreamClosedError should be a subclass of HTTPError with code 599."""
    err = HTTPStreamClosedError("test message")
    assert isinstance(err, HTTPError), "Should inherit from HTTPError"
    assert err.code == 599, "Error code should be 599"
    assert err.message == "test message", "Message should be stored correctly"


def test_httpstreamclosederror_str_returns_message():
    """__str__ should return the provided message."""
    err = HTTPStreamClosedError("custom error")
    assert str(err) == "custom error", "__str__ should return the message"


def test_httpstreamclosederror_str_returns_default_when_no_message():
    """If no message is provided, __str__ should return the default."""
    err = HTTPStreamClosedError("")
    # HTTPError stores message as None if empty string is passed
    assert err.message is None or err.message == "", "Message should be empty or None"
    assert str(err) == "Stream closed", "__str__ should return default when message is empty"
