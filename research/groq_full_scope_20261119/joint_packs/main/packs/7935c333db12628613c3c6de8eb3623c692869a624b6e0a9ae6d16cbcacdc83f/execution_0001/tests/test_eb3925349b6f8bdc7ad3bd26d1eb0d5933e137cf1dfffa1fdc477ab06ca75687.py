import pytest
from tornado.httpclient import HTTPClientError, httputil

class DummyResponse:
    """Simple stand‑in for an HTTPResponse object."""
    def __init__(self, status_code, headers=None):
        self.status_code = status_code
        self.headers = headers or {}

def test_httpclienterror_initialization_with_message():
    """Verify that the error stores the provided message and code."""
    err = HTTPClientError(404, message="Not Found")
    assert err.code == 404
    assert err.message == "Not Found"
    assert err.response is None
    # The base Exception should contain the same arguments
    assert err.args == (404, "Not Found", None)

def test_httpclienterror_str_representation():
    """The string representation should match the expected format."""
    err = HTTPClientError(500)
    # httputil.responses contains a default message for 500
    expected_msg = httputil.responses.get(500, "Unknown")
    assert str(err) == f"HTTP 500: {expected_msg}"
    # Changing the message should update the string
    err.message = "Internal Server Error"
    assert str(err) == "HTTP 500: Internal Server Error"

def test_httpclienterror_response_attribute():
    """An HTTPClientError should expose the response object."""
    resp = DummyResponse(302, headers={"Location": "https://example.com"})
    err = HTTPClientError(302, response=resp)
    assert err.response is resp
    assert err.response.status_code == 302
    assert err.response.headers["Location"] == "https://example.com"
