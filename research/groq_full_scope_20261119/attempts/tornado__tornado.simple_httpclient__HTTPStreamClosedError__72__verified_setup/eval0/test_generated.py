import pytest
from tornado.simple_httpclient import HTTPStreamClosedError
from tornado.httpclient import HTTPError


def test_httpstreamclosederror_inherits_httperror_and_has_code():
    """HTTPStreamClosedError should be a subclass of HTTPError and use code 599."""
    err = HTTPStreamClosedError("test message")
    assert isinstance(err, HTTPError)
    assert err.code == 599
    assert err.message == "test message"


def test_httpstreamclosederror_str_returns_message():
    """The string representation should return the provided message."""
    err = HTTPStreamClosedError("custom error")
    assert str(err) == "custom error"


def test_httpstreamclosederror_str_default_when_no_message():
    """If no message is provided, __str__ should return the default."""
    err = HTTPStreamClosedError("")
    # The base HTTPError stores an empty message; __str__ falls back to "Stream closed"
    assert str(err) == "Stream closed"
