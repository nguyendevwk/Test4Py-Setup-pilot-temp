import asyncio
import json
import urllib.parse
import pytest
from tornado.auth import OAuth2Mixin
from tornado.web import RequestHandler
from tornado import httpclient, escape

class DummyHandler(RequestHandler, OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    _OAUTH_ACCESS_TOKEN_URL = "https://example.com/token"

    def __init__(self, application=None, request=None, **kwargs):
        # RequestHandler requires a request; provide a minimal stub
        self._redirected_to = None
        super().__init__(application, request, **kwargs)

    def redirect(self, url, permanent=False, status=None):
        self._redirected_to = url

    def get_auth_http_client(self):
        return DummyHTTPClient()

class DummyHTTPClient(httpclient.AsyncHTTPClient):
    async def fetch(self, url, method="GET", body=None):
        # Return a fake response with JSON body
        class Response:
            body = json.dumps({"ok": True, "url": url, "method": method, "body": body}).encode()
        return Response()

@pytest.mark.asyncio
async def test_authorize_redirect_builds_url(tmp_path):
    handler = DummyHandler()
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        scope=["email", "profile"],
        response_type="token",
        extra_params={"state": "xyz"}
    )
    parsed = urllib.parse.urlparse(handler._redirected_to)
    query = urllib.parse.parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/auth"
    assert query["response_type"] == ["token"]
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
        code="code123",
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
    assert query["code"] == ["code123"]
    assert query["grant_type"] == ["authorization_code"]

@pytest.mark.asyncio
async def test_oauth2_request_includes_access_token_and_parses_json():
    handler = DummyHandler()
    result = await handler.oauth2_request(
        "https://api.example.com/data",
        access_token="token123",
        post_args={"foo": "bar"},
        extra="value"
    )
    assert isinstance(result, dict)
    assert result["ok"] is True
    # The URL should include the access_token and extra as query params
    assert "access_token=token123" in result["url"]
    assert "extra=value" in result["url"]
    # POST body should be encoded correctly
    assert result["method"] == "POST"
    assert result["body"] == "foo=bar"
