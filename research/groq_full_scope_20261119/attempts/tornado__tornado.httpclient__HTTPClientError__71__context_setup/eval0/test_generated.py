import pytest
from tornado.httpclient import HTTPClientError
from tornado import httputil

def test_httpclienterror_basic_initialization():
    """Verify that HTTPClientError stores code, message, and response correctly."""
    # Use a known HTTP status code to trigger default message lookup
    error = HTTPClientError(404)
    assert error.code == 404
    # Default message should come from httputil.responses
    assert error.message == httputil.responses.get(404, "Unknown")
    assert error.response is None
    # String representation should match the format defined in __str__
    assert str(error) == f"HTTP 404: {error.message}"
    # The repr is aliased to __str__
    assert repr(error) == str(error)

def test_httpclienterror_with_custom_message_and_response():
    """Verify that custom message and response are preserved."""
    # Create a minimal HTTPResponse object for testing
    dummy_response = httputil.HTTPResponse(
        request=None,
        code=500,
        headers=httputil.HTTPHeaders(),
        buffer=bytes(),
        effective_url="http://example.com",
        request_time=0.0,
        time_info={},
        request_headers=httputil.HTTPHeaders(),
    )
    custom_msg = "Custom error message"
    error = HTTPClientError(500, message=custom_msg, response=dummy_response)
    assert error.code == 500
    assert error.message == custom_msg
    assert error.response is dummy_response
    # String representation should use the custom message
    assert str(error) == f"HTTP 500: {custom_msg}"
    # repr should match str
    assert repr(error) == str(error)

def test_httpclienterror_unknown_status_code():
    """Verify behavior when an unknown status code is used."""
    # Use a status code that is not in httputil.responses
    unknown_code = 599
    error = HTTPClientError(unknown_code)
    assert error.code == unknown_code
    # Default message should fallback to "Unknown"
    assert error.message == "Unknown"
    assert error.response is None
    assert str(error) == f"HTTP {unknown_code}: Unknown"
