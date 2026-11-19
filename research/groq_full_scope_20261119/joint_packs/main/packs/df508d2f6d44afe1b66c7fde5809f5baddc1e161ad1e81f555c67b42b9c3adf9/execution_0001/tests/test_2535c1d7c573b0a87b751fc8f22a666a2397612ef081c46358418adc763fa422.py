import pytest
from tornado.httpclient import HTTPClientError
from tornado import httputil

def test_httpclienterror_basic_initialization():
    """Verify that the error stores code, message, and response correctly."""
    # Create a dummy response object with minimal attributes
    class DummyResponse:
        status_code = 404
        headers = {"Content-Type": "text/html"}

    dummy_resp = DummyResponse()
    err = HTTPClientError(404, "Not Found", dummy_resp)

    # Attributes should match constructor arguments
    assert err.code == 404
    assert err.message == "Not Found"
    assert err.response is dummy_resp

    # The string representation should include code and message
    assert str(err) == "HTTP 404: Not Found"
    # __repr__ is aliased to __str__
    assert repr(err) == "HTTP 404: Not Found"

def test_httpclienterror_default_message_from_responses():
    """When message is omitted, it should be looked up in httputil.responses."""
    # Use a known status code that has a description in httputil.responses
    code = 500
    err = HTTPClientError(code)

    # The default message should come from httputil.responses
    expected_msg = httputil.responses.get(code, "Unknown")
    assert err.message == expected_msg
    assert str(err) == f"HTTP {code}: {expected_msg}"

def test_httpclienterror_unknown_status_code():
    """For an unknown status code, the default message should be 'Unknown'."""
    # Pick a code that is unlikely to be in httputil.responses
    code = 599  # used for no response received
    err = HTTPClientError(code)

    # Since 599 is not in httputil.responses, message defaults to 'Unknown'
    assert err.message == "Unknown"
    assert str(err) == f"HTTP {code}: Unknown"
