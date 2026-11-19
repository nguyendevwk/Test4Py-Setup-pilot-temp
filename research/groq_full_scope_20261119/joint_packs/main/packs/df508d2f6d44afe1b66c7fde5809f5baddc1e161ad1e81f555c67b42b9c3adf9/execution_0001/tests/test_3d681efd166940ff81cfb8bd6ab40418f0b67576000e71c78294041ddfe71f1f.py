import io
import time
import pytest
from tornado.httpclient import HTTPResponse, HTTPError
from tornado.httputil import HTTPHeaders

def test_success_response_body_and_headers():
    """A normal 200 response should expose body and headers correctly."""
    buf = io.BytesIO(b"hello world")
    headers = HTTPHeaders({"Content-Type": "text/plain", "X-Test": "123"})
    resp = HTTPResponse(
        request=type("Req", (), {"url": "http://example.com"})(),
        code=200,
        headers=headers,
        buffer=buf,
        effective_url="http://example.com",
        request_time=0.123,
        start_time=time.time(),
    )
    # body should be read from buffer
    assert resp.body == b"hello world"
    # headers should be preserved
    assert resp.headers["Content-Type"] == "text/plain"
    assert resp.headers["X-Test"] == "123"
    # error should be None for 2xx
    assert resp.error is None
    # reason defaults to known description
    assert resp.reason == "OK"
    # request_time and start_time are set
    assert resp.request_time == 0.123
    assert resp.start_time is not None

def test_error_response_code_sets_http_error():
    """A non‑2xx status without an explicit error should create an HTTPError."""
    resp = HTTPResponse(
        request=type("Req", (), {"url": "http://example.com"})(),
        code=404,
        headers=HTTPHeaders(),
        buffer=None,
        effective_url="http://example.com",
    )
    # error should be an HTTPError with the status code
    assert isinstance(resp.error, HTTPError)
    assert resp.error.code == 404
    assert resp.error.response is resp
    # rethrow should raise the same error
    with pytest.raises(HTTPError) as exc:
        resp.rethrow()
    assert exc.value is resp.error

def test_start_and_request_time_are_recorded():
    """start_time should be set to a float and request_time should be preserved."""
    start = time.time()
    resp = HTTPResponse(
        request=type("Req", (), {"url": "http://example.com"})(),
        code=200,
        headers=HTTPHeaders(),
        buffer=io.BytesIO(b"data"),
        effective_url="http://example.com",
        request_time=0.456,
        start_time=start,
    )
    assert isinstance(resp.start_time, float)
    assert resp.start_time == start
    assert resp.request_time == 0.456
