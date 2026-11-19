import pytest
from tornado.httpclient import HTTPClient, HTTPResponse, HTTPError
from tornado.ioloop import IOLoop
from tornado.concurrent import Future
from tornado import gen
from typing import Any, Dict, Optional, Type


class DummyAsyncClient:
    """A minimal async client that mimics AsyncHTTPClient for testing."""
    def __init__(self, **kwargs: Any) -> None:
        self.closed = False
        self.fetch_calls: list = []

    async def fetch(self, request: Any, **kwargs: Any) -> HTTPResponse:
        self.fetch_calls.append((request, kwargs))
        # Return a simple HTTPResponse with status 200 and body "ok"
        return HTTPResponse(
            request=request,
            code=200,
            reason="OK",
            headers={},
            buffer=bytes("ok", "utf-8"),
            request_time=0.0,
            connection_time=0.0,
            time_info={},
        )

    def close(self) -> None:
        self.closed = True


def test_httpclient_fetch_delegates_to_async_client(tmp_path: Any) -> None:
    """HTTPClient.fetch should delegate to the async client and return its response."""
    client = HTTPClient(async_client_class=DummyAsyncClient)
    response = client.fetch("http://example.com")
    assert isinstance(response, HTTPResponse)
    assert response.code == 200
    assert response.body == b"ok"
    # Ensure the async client recorded the call
    assert client._async_client.fetch_calls == [("http://example.com", {})]
    client.close()
    assert client._async_client.closed is True
    assert client._closed is True


def test_httpclient_close_is_idempotent(tmp_path: Any) -> None:
    """Calling close multiple times should not raise and should close resources once."""
    client = HTTPClient(async_client_class=DummyAsyncClient)
    client.close()
    # Second close should be harmless
    client.close()
    assert client._async_client.closed is True
    assert client._closed is True
    # IOLoop should be closed; attempting to run_sync should raise
    with pytest.raises(RuntimeError):
        client._io_loop.run_sync(lambda: None)


def test_httpclient_fetch_raises_http_error_on_non_200(tmp_path: Any) -> None:
    """If the async client returns a non-200 response, HTTPClient.fetch should raise HTTPError."""
    class Non200AsyncClient:
        async def fetch(self, request: Any, **kwargs: Any) -> HTTPResponse:
            return HTTPResponse(
                request=request,
                code=404,
                reason="Not Found",
                headers={},
                buffer=bytes("not found", "utf-8"),
                request_time=0.0,
                connection_time=0.0,
                time_info={},
            )
        def close(self) -> None: ...

    client = HTTPClient(async_client_class=Non200AsyncClient)
    with pytest.raises(HTTPError) as excinfo:
        client.fetch("http://example.com")
    assert excinfo.value.response.code == 404
    assert excinfo.value.response.body == b"not found"
    client.close()
