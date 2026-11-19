import pytest
from tornado.httpclient import HTTPError
from tornado.simple_httpclient import HTTPTimeoutError


def test_http_timeout_error_initialization_and_code():
    """HTTPTimeoutError should initialize with code 599 and store the message."""
    msg = "Request timed out after 5 seconds"
    err = HTTPTimeoutError(msg)
    # Verify that the error is an instance of HTTPError and HTTPTimeoutError
    assert isinstance(err, HTTPError)
    assert isinstance(err, HTTPTimeoutError)
    # The HTTPError constructor sets the status code
    assert err.code == 599
    # The message should be stored in the `message` attribute
    assert err.message == msg


def test_http_timeout_error_str_representation():
    """__str__ should return the message if provided, otherwise a default."""
    # Case 1: message provided
    msg = "Custom timeout message"
    err_with_msg = HTTPTimeoutError(msg)
    assert str(err_with_msg) == msg

    # Case 2: empty message defaults to "Timeout"
    err_without_msg = HTTPTimeoutError("")
    assert str(err_without_msg) == "Timeout"


def test_http_timeout_error_inherits_http_error_behavior():
    """HTTPTimeoutError should behave like a normal HTTPError when used in exception handling."""
    msg = "Timeout occurred"
    err = HTTPTimeoutError(msg)
    try:
        raise err
    except HTTPError as e:
        # The caught exception should be the same instance
        assert e is err
        # The HTTPError base class provides a `reason` attribute
        assert e.reason == msg
        # The HTTPError base class also provides a `code` attribute
        assert e.code == 599
