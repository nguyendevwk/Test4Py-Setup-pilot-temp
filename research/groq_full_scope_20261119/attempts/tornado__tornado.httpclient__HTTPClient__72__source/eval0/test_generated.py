import pytest
from tornado.httpclient import HTTPClient, HTTPResponse, HTTPError
from tornado.ioloop import IOLoop
from tornado.concurrent import Future
from tornado.gen import coroutine
from typing import Any, Dict

# Dummy AsyncHTTPClient that mimics the interface used by HTTPClient
class DummyAsyncHTTPClient:
    def __init__(self, *, status_code: int = 200, body: bytes = b"", raise_error: bool = True):
        self._status_code = status_code
        self._body = body
        self._raise_error = raise_error
        self.closed = False

    @coroutine
    def fetch(self, request: Any, **kwargs: Any) -> HTTPResponse:
        # Simulate asynchronous fetch
        if self._status_code >= 400 and self._raise_error:
            raise HTTPError(self._status_code, response=HTTPResponse(
                request=request,
                code=self._status_code,
                reason="Error",
                headers={},
                buffer=self._body,
            ))
        return HTTPResponse(
            request=request,
            code=self._status_code,
            reason="OK",
            headers={},
            buffer=self._body,
        )

    def close(self) -> None:
        self.closed = True

# Test 1: Normal successful fetch
def test_httpclient_fetch_success():
    client = HTTPClient(async_client_class=lambda **kw: DummyAsyncHTTPClient())
    response = client.fetch("http://example.com")
    assert isinstance(response, HTTPResponse)
    assert response.code == 200
    assert response.body == b""
    client.close()
    assert client._async_client.closed

# Test 2: Error response with raise_error=False
def test_httpclient_fetch_error_no_raise():
    client = HTTPClient(async_client_class=lambda **kw: DummyAsyncHTTPClient(status_code=404, raise_error=False))
    response = client.fetch("http://example.com", raise_error=False)
    assert isinstance(response, HTTPResponse)
    assert response.code == 404
    client.close()
    assert client._async_client.closed

# Test 3: Error response with raise_error=True (default)
def test_httpclient_fetch_error_with_raise():
    client = HTTPClient(async_client_class=lambda **kw: DummyAsyncHTTPClient(status_code=500, raise_error=True))
    with pytest.raises(HTTPError) as excinfo:
        client.fetch("http://example.com")
    assert excinfo.value.code == 500
    assert isinstance(excinfo.value.response, HTTPResponse)
    client.close()
    assert client._async_client.closed
