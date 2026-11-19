import io
import pytest
from tornado.httpclient import HTTPResponse, HTTPError, HTTPClientError
from tornado.httputil import HTTPHeaders
from tornado import httputil

class DummyRequest:
    def __init__(self, url):
        self.url = url

def test_success_response_body_and_headers():
    # Create a response with status 200 and a body
    buf = io.BytesIO(b"hello world")
    headers = HTTPHeaders({"Content-Type": "text/plain"})
    req = DummyRequest("http://example.com")
    resp = HTTPResponse(request=req, code=200, headers=headers, buffer=buf)

    # Body should be read from buffer
    assert resp.body == b"hello world"
    # Headers should be preserved
    assert resp.headers["Content-Type"] == "text/plain"
    # No error should be set for 2xx status
    assert resp.error is None
    # Reason should default to known description
    assert resp.reason == httputil.responses[200]

def test_error_response_auto_error():
    # Create a response with status 404 without explicit error
    req = DummyRequest("http://example.com/notfound")
    resp = HTTPResponse(request=req, code=404)

    # Body should be empty when no buffer
    assert resp.body == b""
    # An HTTPError should be automatically created
    assert isinstance(resp.error, HTTPError)
    # The error should reference the response
    assert resp.error.response is resp
    # The error code and message should match the status
    assert resp.error.code == 404
    assert resp.error.message == httputil.responses[404]

def test_rethrow_raises_http_error():
    # Create a response with status 500 and an explicit error
    req = DummyRequest("http://example.com/error")
    explicit_error = HTTPClientError(500, message="Server error")
    resp = HTTPResponse(request=req, code=500, error=explicit_error)

    # rethrow should raise the same exception instance
    with pytest.raises(HTTPClientError) as excinfo:
        resp.rethrow()
    assert excinfo.value is explicit_error
    # The exception message should be as provided
    assert str(excinfo.value) == "HTTP 500: Server error"
