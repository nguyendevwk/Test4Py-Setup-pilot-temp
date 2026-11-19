import pytest
from tornado.httpclient import HTTPClientError
from tornado import httputil

def test_httpclienterror_initialization_and_attributes():
    # Create an error with a known status code and custom message
    err = HTTPClientError(404, message="Not Found", response=None)
    assert err.code == 404
    assert err.message == "Not Found"
    assert err.response is None
    # The base Exception should contain the same arguments
    assert err.args == (404, "Not Found", None)

def test_httpclienterror_default_message_from_responses():
    # Use a status code that has a standard message in httputil.responses
    err = HTTPClientError(500)
    # The default message should come from httputil.responses
    assert err.message == httputil.responses[500]
    # The string representation should include the code and message
    assert str(err) == f"HTTP 500: {httputil.responses[500]}"

def test_httpclienterror_unknown_status_code():
    # Use a status code not present in httputil.responses
    unknown_code = 999
    err = HTTPClientError(unknown_code)
    # The default message should be "Unknown"
    assert err.message == "Unknown"
    assert str(err) == f"HTTP {unknown_code}: Unknown"
