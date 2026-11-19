import asyncio
import warnings
import urllib.parse
import json
import pytest
from tornado.web import RequestHandler
from tornado.auth import OAuth2Mixin
from tornado import httpclient, escape
from tornado.httputil import url_concat

# Helper handler that mixes in OAuth2Mixin and records redirects
class DummyHandler(RequestHandler, OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    _OAUTH_ACCESS_TOKEN_URL = "https://example.com/token"

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.redirected_to = None

    def redirect(self, url, *args, **kwargs):
        self.redirected_to = url

# Test 1: authorize_redirect builds correct URL and calls redirect
def test_authorize_redirect_builds_url(tmp_path):
    handler = DummyHandler(None, None)
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        scope=["email", "profile"],
        response_type="code",
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

# Test 2: _oauth_request_token_url constructs token URL with all params
def test_oauth_request_token_url_construction():
    handler = DummyHandler(None, None)
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

# Test 3: oauth2_request performs HTTP fetch and decodes JSON
@pytest.mark.asyncio
async def test_oauth2_request_fetch_and_decode(monkeypatch):
    handler = DummyHandler(None, None)

    # Mock AsyncHTTPClient.fetch to return a fake response
    class DummyResponse:
        def __init__(self, body):
            self.body = body

    async def fake_fetch(url, method=None, body=None):
        # Verify that the URL contains the access_token query param
        assert "access_token=XYZ" in url
        # Return a JSON body
        return DummyResponse(json.dumps({"ok": True}).encode("utf-8"))

    monkeypatch.setattr(httpclient.AsyncHTTPClient, "fetch", fake_fetch)

    result = await handler.oauth2_request(
        "https://api.example.com/data",
        access_token="XYZ",
        post_args=None,
        extra="value",
    )
    assert result == {"ok": True}
