import asyncio
import warnings
import urllib.parse
import json
import pytest
from tornado.web import RequestHandler
from tornado.auth import OAuth2Mixin
from tornado import httpclient, escape

class DummyHandler(RequestHandler, OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    _OAUTH_ACCESS_TOKEN_URL = "https://example.com/token"
    def __init__(self, application=None, request=None, **kwargs):
        super().__init__(application, request, **kwargs)
        self.redirected_to = None
    def redirect(self, url, permanent=False, status=302):
        self.redirected_to = url

class DummyHTTPClient(httpclient.AsyncHTTPClient):
    def __init__(self, response_body):
        super().__init__()
        self._response_body = response_body
    async def fetch(self, url, method="GET", body=None):
        class Response:
            def __init__(self, body):
                self.body = body
        return Response(self._response_body)

@pytest.mark.asyncio
async def test_authorize_redirect_with_scope_and_extra_params():
    handler = DummyHandler()
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        extra_params={"state": "xyz"},
        scope=["email", "profile"],
        response_type="token",
    )
    parsed = urllib.parse.urlparse(handler.redirected_to)
    qs = urllib.parse.parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert qs["response_type"] == ["token"]
    assert qs["redirect_uri"] == ["https://myapp.com/callback"]
    assert qs["client_id"] == ["abc123"]
    assert qs["state"] == ["xyz"]
    assert qs["scope"] == ["email profile"]

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
    qs = urllib.parse.parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert qs["redirect_uri"] == ["https://myapp.com/callback"]
    assert qs["client_id"] == ["abc123"]
    assert qs["client_secret"] == ["secret"]
    assert qs["code"] == ["authcode"]
    assert qs["grant_type"] == ["authorization_code"]

@pytest.mark.asyncio
async def test_oauth2_request_get_and_post(monkeypatch):
    # Mock the HTTP client to return a known JSON body
    response_body = json.dumps({"ok": True, "data": {"id": 42}}).encode()
    handler = DummyHandler()
    handler.get_auth_http_client = lambda: DummyHTTPClient(response_body)

    # GET request
    result = await handler.oauth2_request(
        "https://api.example.com/resource",
        access_token="token123",
        foo="bar",
    )
    assert result == {"ok": True, "data": {"id": 42}}
    # Ensure query string was appended
    assert "access_token=token123" in result  # part of body, not URL

    # POST request
    result_post = await handler.oauth2_request(
        "https://api.example.com/resource",
        post_args={"message": "hello"},
    )
    assert result_post == {"ok": True, "data": {"id": 42}}
