import asyncio
import json
import urllib.parse
import pytest
from tornado.auth import OAuth2Mixin
from tornado.web import RequestHandler
from tornado import httpclient, escape

class DummyHandler(RequestHandler, OAuth2Mixin):
    """A minimal RequestHandler that records redirects and provides a mock HTTP client."""
    _OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    _OAUTH_ACCESS_TOKEN_URL = "https://example.com/token"

    def __init__(self, application=None, request=None, **kwargs):
        super().__init__(application, request, **kwargs)
        self.redirected_to = None

    def redirect(self, url, permanent=False, status=302):
        self.redirected_to = url

    def get_auth_http_client(self):
        return self.mock_http_client

class MockHTTPClient(httpclient.AsyncHTTPClient):
    """Mock HTTP client that records fetch calls and returns a preset response."""
    def __init__(self, response_body):
        super().__init__()
        self.response_body = response_body
        self.last_fetch = None

    async def fetch(self, url, method="GET", body=None):
        self.last_fetch = {"url": url, "method": method, "body": body}
        class Response:
            body = self.response_body
        return Response()

@pytest.mark.asyncio
async def test_authorize_redirect_builds_correct_url():
    handler = DummyHandler()
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        scope=["email", "profile"],
        response_type="code",
        extra_params={"state": "xyz"}
    )
    parsed = urllib.parse.urlparse(handler.redirected_to)
    query = urllib.parse.parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/auth"
    assert query["response_type"] == ["code"]
    assert query["redirect_uri"] == ["https://myapp.com/callback"]
    assert query["client_id"] == ["abc123"]
    assert query["scope"] == ["email profile"]
    assert query["state"] == ["xyz"]

def test_oauth_request_token_url_construction():
    handler = DummyHandler()
    url = handler._oauth_request_token_url(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        client_secret="secret",
        code="authcode",
        extra_params={"grant_type": "authorization_code"}
    )
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/token"
    assert query["redirect_uri"] == ["https://myapp.com/callback"]
    assert query["client_id"] == ["abc123"]
    assert query["client_secret"] == ["secret"]
    assert query["code"] == ["authcode"]
    assert query["grant_type"] == ["authorization_code"]

@pytest.mark.asyncio
async def test_oauth2_request_uses_http_client_and_parses_json():
    # Prepare a mock response body
    response_data = {"ok": True, "data": {"id": 42}}
    mock_client = MockHTTPClient(json.dumps(response_data).encode("utf-8"))
    handler = DummyHandler()
    handler.mock_http_client = mock_client

    result = await handler.oauth2_request(
        "https://api.example.com/resource",
        access_token="token123",
        post_args={"foo": "bar"},
        extra="value"
    )

    # Verify that the HTTP client was called correctly
    fetch_call = mock_client.last_fetch
    assert fetch_call["method"] == "POST"
    assert fetch_call["body"] == urllib.parse.urlencode({"foo": "bar"})
    # URL should contain access_token and extra as query parameters
    parsed = urllib.parse.urlparse(fetch_call["url"])
    query = urllib.parse.parse_qs(parsed.query)
    assert query["access_token"] == ["token123"]
    assert query["extra"] == ["value"]

    # Verify that the JSON response was decoded correctly
    assert result == response_data
