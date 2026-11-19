import asyncio
import json
import urllib.parse

import pytest
from tornado import escape
from tornado.web import RequestHandler

from tornado.auth import OAuth2Mixin


class DummyHandler(RequestHandler, OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    _OAUTH_ACCESS_TOKEN_URL = "https://example.com/token"

    def __init__(self, **kwargs):
        # RequestHandler requires a request argument; we can pass None for tests
        super().__init__(None, None)

    def redirect(self, url, *args, **kwargs):
        # Store the last redirected URL for assertions
        self._last_redirect = url


class DummyHTTPClient:
    def __init__(self, response_body: bytes):
        self._response_body = response_body

    async def fetch(self, url, method="GET", body=None):
        class Response:
            body = self._response_body

        return Response()


@pytest.fixture
def handler():
    return DummyHandler()


def test_authorize_redirect_builds_correct_url(handler):
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        scope=["email", "profile"],
        response_type="token",
        extra_params={"state": "xyz"},
    )
    parsed = urllib.parse.urlparse(handler._last_redirect)
    query = urllib.parse.parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/auth"
    assert query["response_type"] == ["token"]
    assert query["redirect_uri"] == ["https://myapp.com/callback"]
    assert query["client_id"] == ["abc123"]
    assert query["scope"] == ["email profile"]
    assert query["state"] == ["xyz"]


def test_oauth_request_token_url_construction(handler):
    url = handler._oauth_request_token_url(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        client_secret="secret",
        code="code123",
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
    assert query["code"] == ["code123"]
    assert query["grant_type"] == ["authorization_code"]


@pytest.mark.asyncio
async def test_oauth2_request_returns_decoded_json(handler):
    expected = {"ok": True, "data": {"id": 1}}
    handler.get_auth_http_client = lambda: DummyHTTPClient(
        response_body=json.dumps(expected).encode()
    )
    result = await handler.oauth2_request(
        "https://api.example.com/resource",
        access_token="token123",
        post_args={"foo": "bar"},
    )
    assert result == expected
