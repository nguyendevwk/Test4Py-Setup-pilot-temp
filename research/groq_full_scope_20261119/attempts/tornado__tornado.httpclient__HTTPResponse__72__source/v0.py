import pytest
from tornado.httpclient import HTTPResponse, HTTPError
from tornado.httputil import HTTPHeaders
from io import BytesIO

def test_success_response_body_and_reason():
    headers = HTTPHeaders({"Content-Type": "text/plain"})
    buf = BytesIO(b"hello world")
    resp = HTTPResponse(
        request=type("Req", (), {"url": "http://example.com"})(),
        code=200,
        headers=headers,
        buffer=buf,
        reason="OK",
        start_time=0.0,
        request_time=0.1,
    )
    # body should be read lazily from buffer
    assert resp.body == b"hello world"
    # body cached after first access
    buf.truncate(0)
    assert resp.body == b"hello world"
    # reason is set explicitly
    assert resp.reason == "OK"
    # no error for 2xx
    assert resp.error is None
    # effective_url defaults to request.url
    assert resp.effective_url == "http://example.com"

def test_error_response_code_sets_http_error():
    resp = HTTPResponse(
        request=type("Req", (), {"url": "http://example.com"})(),
        code=404,
        headers=HTTPHeaders(),
        buffer=BytesIO(b"not found"),
    )
    # error should be an HTTPError with the status code
    assert isinstance(resp.error, HTTPError)
    assert resp.error.code == 404
    assert resp.error.response is resp
    # rethrow should raise the same error
    with pytest.raises(HTTPError) as exc:
        resp.rethrow()
    assert exc.value is resp.error

def test_custom_error_overrides_status_code():
    custom_exc = ValueError("custom failure")
    resp = HTTPResponse(
        request=type("Req", (), {"url": "http://example.com"})(),
        code=500,
        headers=HTTPHeaders(),
        buffer=BytesIO(b"server error"),
        error=custom_exc,
    )
    # custom error should be used instead of HTTPError
    assert resp.error is custom_exc
    # rethrow should raise the custom exception
    with pytest.raises(ValueError) as exc:
        resp.rethrow()
    assert exc.value is custom_exc
