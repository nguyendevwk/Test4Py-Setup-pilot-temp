import asyncio
import urllib.parse
import pytest
from tornado.auth import OAuth2Mixin
from tornado.web import RequestHandler
from tornado import escape
from tornado.httputil import url_concat

class DummyHandler(RequestHandler, OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    _OAUTH_ACCESS_TOKEN_URL = "https://example.com/token"

    def __init__(self, *args, **kwargs):
        # RequestHandler requires a request argument; we can pass None for tests
        super().__init__(None, None)

    def redirect(self, url, permanent=False):
        # Store the last redirected URL for inspection
        self._redirected_url = url

    def get_auth_http_client(self):
        # Return a dummy client that records fetch calls
        return DummyHTTPClient()

class DummyHTTPClient:
    async def fetch(self, url, method="GET", body=None):
        # Return a dummy response object with a body attribute
        class Response:
            def __init__(self, body):
                self.body = body
        # Echo back the URL and body as JSON for inspection
        data = {"url": url, "method": method, "body": body}
        return Response(escape.json_encode(data).encode())

@pytest.mark.asyncio
async def test_authorize_redirect_builds_correct_url(tmp_path):
    handler = DummyHandler()
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        scope=["email", "profile"],
        response_type="token",
    )
    # The redirect URL should contain all parameters correctly encoded
    parsed = urllib.parse.urlparse(handler._redirected_url)
    query = urllib.parse.parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/auth"
    assert query["response_type"] == ["token"]
    assert query["redirect_uri"] == ["https://myapp.com/callback"]
    assert query["client_id"] == ["abc123"]
    assert query["scope"] == ["email profile"]

def test_oauth_request_token_url_construction():
    handler = DummyHandler()
    url = handler._oauth_request_token_url(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        client_secret="secret",
        code="authcode",
        extra_params={"grant_type": "authorization_code"},
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
    handler = DummyHandler()
    # Perform a GET request with an access token
    result = await handler.oauth2_request(
        "https://api.example.com/data",
        access_token="token123",
        param1="value1",
    )
    # The dummy client echoes back the URL and method
    assert result["method"] == "GET"
    assert "access_token=token123" in result["url"]
    assert "param1=value1" in result["url"]

    # Perform a POST request with body arguments
    result_post = await handler.oauth2_request(
        "https://api.example.com/data",
        post_args={"field": "data"},
    )
    assert result_post["method"] == "POST"
    assert result_post["body"] == "field=data"
