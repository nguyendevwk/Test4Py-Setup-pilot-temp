import asyncio
import urllib.parse
import json
import pytest
from tornado.web import RequestHandler
from tornado.auth import OAuth2Mixin
from tornado import httpclient, escape

# Dummy handler that records the redirect URL
class DummyHandler(RequestHandler, OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    _OAUTH_ACCESS_TOKEN_URL = "https://example.com/token"

    def __init__(self, application=None, request=None, **kwargs):
        # RequestHandler requires a request; use a minimal stub
        from tornado.httputil import HTTPServerRequest
        if request is None:
            request = HTTPServerRequest(method="GET", uri="/")
        super().__init__(application, request, **kwargs)
        self.redirected_to = None

    def redirect(self, url, permanent=False, status=None):
        self.redirected_to = url

# Custom HTTP client that returns a predictable response
class DummyHTTPClient(httpclient.AsyncHTTPClient):
    async def fetch(self, url, method="GET", body=None):
        # Return a JSON body that echoes the URL and body
        body_dict = {"url": url, "method": method, "body": body}
        return httpclient.HTTPResponse(
            request=None,
            code=200,
            headers={},
            buffer=bytes(json.dumps(body_dict), "utf-8"),
        )

# Override get_auth_http_client to use DummyHTTPClient
class TestHandler(DummyHandler):
    def get_auth_http_client(self):
        return DummyHTTPClient()

@pytest.mark.asyncio
async def test_authorize_redirect_builds_correct_url(tmp_path):
    handler = DummyHandler()
    # Call with all parameters
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        extra_params={"foo": "bar"},
        scope=["read", "write"],
        response_type="token",
    )
    # Parse the redirected URL
    parsed = urllib.parse.urlparse(handler.redirected_to)
    query = urllib.parse.parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/auth"
    assert query["response_type"] == ["token"]
    assert query["redirect_uri"] == ["https://myapp.com/callback"]
    assert query["client_id"] == ["abc123"]
    assert query["foo"] == ["bar"]
    assert query["scope"] == ["read write"]

def test_oauth_request_token_url_construction():
    handler = DummyHandler()
    url = handler._oauth_request_token_url(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        client_secret="secret",
        code="code123",
        extra_params={"state": "xyz"},
    )
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/token"
    assert query["redirect_uri"] == ["https://myapp.com/callback"]
    assert query["client_id"] == ["abc123"]
    assert query["client_secret"] == ["secret"]
    assert query["code"] == ["code123"]
    assert query["state"] == ["xyz"]

@pytest.mark.asyncio
async def test_oauth2_request_uses_access_token_and_post_args():
    handler = TestHandler()
    # Perform a POST request
    result = await handler.oauth2_request(
        "https://api.example.com/resource",
        access_token="token123",
        post_args={"key": "value"},
        extra="param",
    )
    # The dummy client echoes back the request details
    assert result["method"] == "POST"
    # URL should include access_token and extra param
    assert "access_token=token123" in result["url"]
    assert "extra=param" in result["url"]
    # Body should be URL encoded post_args
    assert result["body"] == "key=value"
