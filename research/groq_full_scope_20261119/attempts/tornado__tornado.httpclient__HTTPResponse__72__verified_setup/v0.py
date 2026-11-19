import pytest
from io import BytesIO
from tornado.httpclient import HTTPResponse, HTTPError
from tornado import httputil

def test_success_response_body_and_headers():
    headers = httputil.HTTPHeaders({"Content-Type": "text/plain", "X-Test": "123"})
    buffer = BytesIO(b"Hello, world!")
    resp = HTTPResponse(
        request=type("Req", (), {"url": "http://example.com"})(),
        code=200,
        headers=headers,
        buffer=buffer,
        effective_url="http://example.com",
        request_time=0.1,
        time_info={"dns": 0.01, "connect": 0.02},
    )
    # Body should be read lazily from buffer
    assert resp.body == b"Hello, world!"
    # Headers should be preserved
    assert resp.headers["Content-Type"] == "text/plain"
    assert resp.headers["X-Test"] == "123"
    # No error should be set for 2xx status
    assert resp.error is None
    # Reason should be the default for 200
    assert resp.reason == httputil.responses[200]
    # time_info should be stored
    assert resp.time_info["dns"] == 0.01
    assert resp.time_info["connect"] == 0.02

def test_error_response_code_triggers_http_error():
    resp = HTTPResponse(
        request=type("Req", (), {"url": "http://example.com"})(),
        code=404,
        reason="Not Found",
    )
    # For non-2xx status, error should be an HTTPError
    assert isinstance(resp.error, HTTPError)
    assert resp.error.code == 404
    assert resp.error.message == "Not Found"
    # The response object should be attached to the error
    assert resp.error.response is resp
    # rethrow should raise the same error
    with pytest.raises(HTTPError) as excinfo:
        resp.rethrow()
    assert excinfo.value is resp.error

def test_body_property_caches_value_and_handles_none_buffer():
    # When buffer is None, body should be empty bytes
    resp_empty = HTTPResponse(
        request=type("Req", (), {"url": "http://example.com"})(),
        code=200,
        buffer=None,
    )
    assert resp_empty.body == b""
    # When buffer is provided, body should be cached after first access
    buffer = BytesIO(b"cached")
    resp = HTTPResponse(
        request=type("Req", (), {"url": "http://example.com"})(),
        code=200,
        buffer=buffer,
    )
    first = resp.body
    # Modify the underlying buffer to ensure caching
    buffer.truncate(0)
    buffer.write(b"modified")
    # Body should still return the original cached value
    assert resp.body == first == b"cached"
