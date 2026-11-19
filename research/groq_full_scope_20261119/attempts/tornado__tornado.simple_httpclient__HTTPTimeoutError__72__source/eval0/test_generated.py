import pytest
from tornado.simple_httpclient import HTTPTimeoutError


def test_http_timeout_error_initialization():
    """HTTPTimeoutError should store the provided message and use code 599."""
    err = HTTPTimeoutError("Request timed out")
    assert isinstance(err, HTTPTimeoutError)
    assert err.code == 599
    assert err.message == "Request timed out"
    # The base HTTPError stores the message in .message attribute
    assert err.args[0] == 599
    assert err.args[1] == "Request timed out"


def test_http_timeout_error_str_without_message():
    """When no message is supplied, __str__ should return the default 'Timeout'."""
    err = HTTPTimeoutError("")
    # The message attribute is an empty string, so __str__ falls back to "Timeout"
    assert str(err) == "Timeout"
    # Explicitly check that the message attribute is indeed empty
    assert err.message == ""


def test_http_timeout_error_str_with_message():
    """When a message is supplied, __str__ should return that message."""
    err = HTTPTimeoutError("Connection lost")
    assert str(err) == "Connection lost"
    assert err.message == "Connection lost"
