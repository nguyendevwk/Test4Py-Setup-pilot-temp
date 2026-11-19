import pytest
import asyncio
from tornado.httpclient import HTTPClient, HTTPResponse

class DummyAsyncClient:
    """A minimal async client used for testing HTTPClient."""
    def __init__(self, *, return_body: str = "ok", raise_exc: Exception | None = None):
        self.return_body = return_body
        self.raise_exc = raise_exc
        self.closed = False

    async def fetch(self, request, **kwargs):
        if self.raise_exc:
            raise self.raise_exc
        # Return a simple HTTPResponse-like object
        return HTTPResponse(
            request=request,
            code=200,
            reason="OK",
            headers={},
            buffer=bytes(self.return_body, "utf-8"),
            request_time=0.0,
            elapsed=0.0,
            connection_time=0.0,
            request_size=0,
            response_size=len(self.return_body),
        )

    def close(self):
        self.closed = True

def test_httpclient_fetch_returns_expected_response(tmp_path):
    """HTTPClient should return the response from the async client."""
    client = HTTPClient(async_client_class=DummyAsyncClient, return_body="hello")
    response = client.fetch("http://example.com")
    assert isinstance(response, HTTPResponse)
    assert response.body == b"hello"
    client.close()
    assert client._closed is True

def test_httpclient_close_does_not_prevent_fetch(tmp_path):
    """Closing the client should not raise errors when fetching again."""
    client = HTTPClient(async_client_class=DummyAsyncClient, return_body="world")
    client.close()
    # After close, the underlying async client still exists; fetch should still work
    response = client.fetch("http://example.com")
    assert response.body == b"world"
    client.close()  # closing again should be safe

def test_httpclient_fetch_propagates_exceptions(tmp_path):
    """HTTPClient.fetch should propagate exceptions from the async client."""
    exc = RuntimeError("network failure")
    client = HTTPClient(async_client_class=DummyAsyncClient, raise_exc=exc)
    with pytest.raises(RuntimeError, match="network failure"):
        client.fetch("http://example.com")
    client.close()
