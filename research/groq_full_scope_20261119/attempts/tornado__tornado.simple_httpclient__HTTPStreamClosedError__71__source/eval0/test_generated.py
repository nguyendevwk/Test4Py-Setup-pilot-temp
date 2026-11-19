import pytest
from tornado.httpclient import HTTPError
from tornado.simple_httpclient import HTTPStreamClosedError


def test_httpstreamclosederror_inherits_and_has_code_and_message():
    """HTTPStreamClosedError should inherit HTTPError and set status code 599."""
    err = HTTPStreamClosedError("stream closed")
    # Inherits from HTTPError
    assert isinstance(err, HTTPError)
    # Status code should be 599
    assert err.code == 599
    # Message should be stored
    assert err.message == "stream closed"
    # The string representation should be the message
    assert str(err) == "stream closed"


def test_httpstreamclosederror_str_default_message():
    """When no message is provided, __str__ should return a default."""
    err = HTTPStreamClosedError("")
    # message attribute is empty string
    assert err.message == ""
    # __str__ should fallback to default
    assert str(err) == "Stream closed"


def test_httpstreamclosederror_repr_and_eq():
    """Ensure that representation and equality behave as expected."""
    err1 = HTTPStreamClosedError("closed")
    err2 = HTTPStreamClosedError("closed")
    err3 = HTTPStreamClosedError("different")
    # __repr__ should include class name and message
    assert "HTTPStreamClosedError" in repr(err1)
    assert "closed" in repr(err1)
    # Equality should be based on type and message
    assert err1 == err2
    assert err1 != err3
