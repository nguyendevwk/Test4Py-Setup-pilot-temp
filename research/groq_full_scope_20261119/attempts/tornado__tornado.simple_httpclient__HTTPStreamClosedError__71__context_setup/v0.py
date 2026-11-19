import pytest
from tornado.simple_httpclient import HTTPStreamClosedError


def test_httpstreamclosederror_initialization_and_code():
    """Verify that the error is initialized with the correct status code."""
    err = HTTPStreamClosedError("test message")
    # HTTPError stores the status code in the `status_code` attribute
    assert err.status_code == 599
    # The message should be stored in the `message` attribute
    assert err.message == "test message"


def test_httpstreamclosederror_str_representation():
    """Verify that the string representation uses the message."""
    err = HTTPStreamClosedError("stream lost")
    # __str__ should return the message
    assert str(err) == "stream lost"
    # If message is empty, it should default to "Stream closed"
    empty_err = HTTPStreamClosedError("")
    assert str(empty_err) == "Stream closed"


def test_httpstreamclosederror_inherits_httperror():
    """Ensure that HTTPStreamClosedError behaves like an HTTPError."""
    err = HTTPStreamClosedError("oops")
    # HTTPError is a subclass of Exception
    assert isinstance(err, Exception)
    # It should also be an instance of HTTPError
    from tornado.httpclient import HTTPError
    assert isinstance(err, HTTPError)
    # The error should be truthy and have a non-empty string representation
    assert bool(err)
    assert str(err) != ""
