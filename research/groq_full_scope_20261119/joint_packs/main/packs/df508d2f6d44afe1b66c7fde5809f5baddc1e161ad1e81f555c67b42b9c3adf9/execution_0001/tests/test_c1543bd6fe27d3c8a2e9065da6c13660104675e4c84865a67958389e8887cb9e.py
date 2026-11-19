import pytest
from tornado.httpclient import HTTPClient
from tornado.ioloop import IOLoop
from tornado import gen


class DummyAsyncClient:
    """A minimal async client used for testing HTTPClient."""
    def __init__(self, **kwargs):
        self.closed = False
        self.fetch_calls = []

    async def fetch(self, request, **kwargs):
        self.fetch_calls.append((request, kwargs))
        # Return a simple object to act as a response
        return {"url": request, "status": 200, "body": b"ok"}

    def close(self):
        self.closed = True


def test_fetch_delegates_to_async_client(tmp_path):
    """HTTPClient.fetch should delegate to the async client and return its result."""
    client = HTTPClient(async_client_class=DummyAsyncClient)
    response = client.fetch("http://example.com")
    # The dummy async client returns a dict; verify its contents
    assert isinstance(response, dict)
    assert response["url"] == "http://example.com"
    assert response["status"] == 200
    assert response["body"] == b"ok"
    # Ensure the async client recorded the call
    assert client._async_client.fetch_calls == [("http://example.com", {})]
    client.close()


def test_close_frees_resources_and_is_idempotent(tmp_path):
    """HTTPClient.close should close the async client and the IOLoop, and be safe to call twice."""
    client = HTTPClient(async_client_class=DummyAsyncClient)
    # Initially not closed
    assert not client._closed
    assert not client._async_client.closed
    # First close
    client.close()
    assert client._closed
    assert client._async_client.closed
    # Second close should not raise and keep state
    client.close()
    assert client._closed
    assert client._async_client.closed


def test_fetch_with_additional_kwargs_passed(tmp_path):
    """HTTPClient.fetch should forward additional kwargs to the async client."""
    client = HTTPClient(async_client_class=DummyAsyncClient)
    response = client.fetch("http://example.com", timeout=5, headers={"X-Test": "1"})
    assert response["url"] == "http://example.com"
    # Verify that the async client received the kwargs
    assert client._async_client.fetch_calls[0][1] == {"timeout": 5, "headers": {"X-Test": "1"}}
    client.close()
