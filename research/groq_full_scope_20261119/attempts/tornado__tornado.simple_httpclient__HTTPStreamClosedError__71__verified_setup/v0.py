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
    """The string representation should return the message or a default."""
    err_with_msg = HTTPStreamClosedError("stream closed")
    assert str(err_with_msg) == "stream closed"

    err_without_msg = HTTPStreamClosedError("")
    # When message is empty, __str__ should return the default
    assert str(err_without_msg) == "Stream closed"


def test_httpstreamclosederror_inherits_httperror():
    """Ensure that HTTPStreamClosedError is a subclass of HTTPError."""
    err = HTTPStreamClosedError("oops")
    # HTTPError is imported from tornado.httpclient
    from tornado.httpclient import HTTPError
    assert isinstance(err, HTTPError)
    # The error should also be considered an HTTPClientError
    from tornado.httpclient import HTTPClientError
    assert isinstance(err, HTTPClientError)
