import pytest
from tornado.httpclient import HTTPClient, HTTPError, HTTPResponse
from tornado.httputil import HTTPRequest


class DummyAsyncClient:
    """A minimal AsyncHTTPClient replacement for testing."""
    def __init__(self, *, raise_error: bool = True):
        self._closed = False
        self.raise_error = raise_error

    async def fetch(self, request, **kwargs):
        if isinstance(request, str):
            request = HTTPRequest(request, **kwargs)
        if self.raise_error:
            # Simulate a non‑200 response that should raise HTTPError
            raise HTTPError(404, "Not Found", response=HTTPResponse(
                request=request, code=404, reason="Not Found", headers={}, buffer=b"")
            )
        # Return a successful response
        return HTTPResponse(
            request=request,
            code=200,
            reason="OK",
            headers={},
            buffer=b"Hello, world!"
        )

    def close(self):
        self._closed = True


def test_fetch_success(tmp_path):
    """HTTPClient.fetch should return a successful HTTPResponse."""
    client = HTTPClient(async_client_class=DummyAsyncClient, raise_error=False)
    try:
        response = client.fetch("http://example.com")
        assert isinstance(response, HTTPResponse)
        assert response.code == 200
        assert response.body == b"Hello, world!"
    finally:
        client.close()
        assert client._closed is True


def test_fetch_error_raises_http_error(tmp_path):
    """HTTPClient.fetch should raise HTTPError when raise_error is True."""
    client = HTTPClient(async_client_class=DummyAsyncClient, raise_error=True)
    try:
        with pytest.raises(HTTPError) as excinfo:
            client.fetch("http://example.com")
        assert excinfo.value.code == 404
        assert excinfo.value.response.code == 404
    finally:
        client.close()
        assert client._closed is True


def test_fetch_error_no_raise(tmp_path):
    """HTTPClient.fetch should not raise when raise_error=False."""
    client = HTTPClient(async_client_class=DummyAsyncClient, raise_error=False)
    try:
        # Even though DummyAsyncClient raises HTTPError, HTTPClient should suppress it
        response = client.fetch("http://example.com")
        assert isinstance(response, HTTPResponse)
        assert response.code == 200
    finally:
        client.close()
        assert client._closed is True
