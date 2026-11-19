import asyncio
import urllib.parse
import pytest
from tornado.auth import OAuth2Mixin
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient, HTTPResponse
from tornado import escape


class DummyHandler(OAuth2Mixin, RequestHandler):
    """A minimal RequestHandler that records redirects."""
    def __init__(self, *args, **kwargs):
        # RequestHandler requires an app; we pass None and override needed methods.
        super().__init__(app=None, request=None, **kwargs)
        self.redirected_to = None

    def redirect(self, url, *args, **kwargs):
        self.redirected_to = url


@pytest.mark.asyncio
async def test_authorize_redirect_constructs_correct_url(tmp_path):
    """authorize_redirect should build the correct redirect URL."""
    handler = DummyHandler()
    handler._OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        scope=["email", "profile"],
        response_type="token",
    )
    parsed = urllib.parse.urlparse(handler.redirected_to)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/auth"
    qs = urllib.parse.parse_qs(parsed.query)
    assert qs["response_type"] == ["token"]
    assert qs["redirect_uri"] == ["https://myapp.com/callback"]
    assert qs["client_id"] == ["abc123"]
    assert qs["scope"] == ["email profile"]


def test_oauth_request_token_url_includes_all_params():
    """_oauth_request_token_url should include all provided parameters."""
    handler = DummyHandler()
    handler._OAUTH_ACCESS_TOKEN_URL = "https://example.com/token"
    url = handler._oauth_request_token_url(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        client_secret="secret",
        code="code123",
        extra_params={"foo": "bar"},
    )
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    assert qs["redirect_uri"] == ["https://myapp.com/callback"]
    assert qs["client_id"] == ["abc123"]
    assert qs["client_secret"] == ["secret"]
    assert qs["code"] == ["code123"]
    assert qs["foo"] == ["bar"]


@pytest.mark.asyncio
async def test_oauth2_request_uses_access_token_and_post_args():
    """oauth2_request should append access_token and POST body correctly."""
    handler = DummyHandler()

    async def fake_fetch(url, method=None, body=None):
        # Verify that the URL contains the access_token query param
        assert "access_token=XYZ" in url
        # Verify that the body is correctly URL encoded
        assert body == urllib.parse.urlencode({"msg": "hello"})
        # Return a fake HTTPResponse
        return HTTPResponse(
            request=None,
            code=200,
            headers={},
            body=b'{"ok":true}',
            time=0,
        )

    # Patch the HTTP client to use our fake_fetch
    class FakeClient:
        async def fetch(self, *args, **kwargs):
            return await fake_fetch(*args, **kwargs)

    handler.get_auth_http_client = lambda: FakeClient()
    result = await handler.oauth2_request(
        "https://api.example.com/data",
        access_token="XYZ",
        post_args={"msg": "hello"},
    )
    assert result == {"ok": True}
