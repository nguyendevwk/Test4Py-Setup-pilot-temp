import pytest
from tornado.simple_httpclient import HTTPTimeoutError
from tornado.httpclient import HTTPError

def test_http_timeout_error_initialization_and_str():
    """Verify that HTTPTimeoutError correctly sets the status code and message."""
    err = HTTPTimeoutError("timeout occurred")
    # HTTPError stores the status code in `status_code`
    assert err.status_code == 599
    # The message attribute should be preserved
    assert err.message == "timeout occurred"
    # String representation should return the message
    assert str(err) == "timeout occurred"

def test_http_timeout_error_empty_message():
    """An empty message should default to 'Timeout' in __str__."""
    err = HTTPTimeoutError("")
    # Even with an empty message, status code remains 599
    assert err.status_code == 599
    # The message attribute is an empty string
    assert err.message == ""
    # __str__ should fall back to the default 'Timeout'
    assert str(err) == "Timeout"

def test_http_timeout_error_is_subclass_of_http_error():
    """Ensure HTTPTimeoutError is a subclass of HTTPError and behaves accordingly."""
    err = HTTPTimeoutError("test")
    # Instance should be recognized as HTTPError
    assert isinstance(err, HTTPError)
    # It should also be recognized as a generic Exception
    assert isinstance(err, Exception)
    # The error code should be accessible via the HTTPError interface
    assert err.code == 599
