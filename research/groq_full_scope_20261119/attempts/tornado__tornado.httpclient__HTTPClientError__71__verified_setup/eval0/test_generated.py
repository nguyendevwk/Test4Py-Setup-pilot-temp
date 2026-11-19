import pytest
from tornado.httpclient import HTTPClientError, httputil

def test_httpclienterror_default_message():
    """When no message is provided, the default HTTP status text is used."""
    err = HTTPClientError(404)
    assert err.code == 404
    assert err.message == httputil.responses.get(404, "Unknown")
    assert str(err) == f"HTTP 404: {err.message}"
    assert err.response is None

def test_httpclienterror_custom_message_and_response():
    """Custom message and response are preserved and reflected in the string."""
    dummy_response = httputil.HTTPResponse(
        code=200,
        request=httputil.HTTPRequest(url="http://example.com"),
        headers=httputil.HTTPHeaders(),
        buffer=bytes(),
    )
    err = HTTPClientError(500, message="Server error", response=dummy_response)
    assert err.code == 500
    assert err.message == "Server error"
    assert err.response is dummy_response
    assert str(err) == "HTTP 500: Server error"

def test_httpclienterror_unknown_status_code():
    """An unknown status code falls back to 'Unknown' message."""
    unknown_code = 9999
    err = HTTPClientError(unknown_code)
    assert err.code == unknown_code
    assert err.message == "Unknown"
    assert str(err) == f"HTTP {unknown_code}: Unknown"
