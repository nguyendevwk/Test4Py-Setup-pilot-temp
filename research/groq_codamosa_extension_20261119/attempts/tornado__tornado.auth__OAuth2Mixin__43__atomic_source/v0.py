import asyncio
import warnings
import urllib.parse
import json
import pytest
from tornado.web import RequestHandler
from tornado.auth import OAuth2Mixin
from tornado import httpclient, escape
from tornado.httputil import url_concat


class DummyHandler(RequestHandler, OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    _OAUTH_ACCESS_TOKEN_URL = "https://example.com/token"

    def initialize(self):
        self.redirected_to = None

    def redirect(self, url, permanent=False, **kwargs):
        self.redirected_to = url


def test_authorize_redirect_includes_all_params(tmp_path):
    handler = DummyHandler()
    handler.initialize()
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        extra_params={"state": "xyz"},
        scope=["read", "write"],
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
    assert query["state"] == ["xyz"]
    assert query["scope"] == ["read write"]


def test_oauth_request_token_url_omits_none_params():
    handler = DummyHandler()
    url = handler._oauth_request_token_url(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        client_secret=None,
        code=None,
        extra_params={"grant_type": "authorization_code"},
    )
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/token"
    assert query["redirect_uri"] == ["https://myapp.com/callback"]
    assert query["client_id"] == ["abc123"]
    assert query["grant_type"] == ["authorization_code"]
    assert "client_secret" not in query
    assert "code" not in query


@pytest.mark.asyncio
async def test_oauth2_request_uses_access_token_and_post_args(monkeypatch):
    handler = DummyHandler()
    # Mock the HTTP client to return a predictable response
    class DummyResponse:
        body = json.dumps({"ok": True}).encode()

    class DummyClient:
        async def fetch(self, url, method="GET", body=None):
            # Verify that the URL contains the access_token query param
            assert "access_token=secret" in url
            # Verify that POST body is correctly encoded
            assert body == urllib.parse.urlencode({"msg": "hello"})
            return DummyResponse()

    monkeypatch.setattr(handler, "get_auth_http_client", lambda: DummyClient())
    result = await handler.oauth2_request(
        "https://api.example.com/data",
        access_token="secret",
        post_args={"msg": "hello"},
    )
    assert result == {"ok": True}
