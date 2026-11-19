import asyncio
import urllib.parse
import pytest
from tornado.auth import OAuth2Mixin
from tornado import escape
from tornado.httpclient import AsyncHTTPClient, HTTPResponse
from unittest.mock import AsyncMock, MagicMock


class DummyHandler(OAuth2Mixin):
    """A minimal handler that records redirects and supplies a mock HTTP client."""
    _OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    _OAUTH_ACCESS_TOKEN_URL = "https://example.com/token"

    def __init__(self):
        self.redirected_to = None

    def redirect(self, url: str) -> None:
        self.redirected_to = url

    def get_auth_http_client(self) -> AsyncHTTPClient:
        return self._http_client

    def set_http_client(self, client: AsyncHTTPClient) -> None:
        self._http_client = client


@pytest.mark.asyncio
async def test_authorize_redirect_with_scope_and_extra_params():
    handler = DummyHandler()
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        scope=["email", "profile"],
        extra_params={"state": "xyz"},
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
    # scope should be space‑separated
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
    mock_client = AsyncMock(spec=AsyncHTTPClient)
    handler.set_http_client(mock_client)

    # Prepare a fake HTTPResponse with JSON body
    fake_body = escape.json_encode({"ok": True, "data": {"id": 42}})
    mock_response = HTTPResponse(request=None, code=200, headers={}, body=fake_body)
    mock_client.fetch.return_value = asyncio.Future()
    mock_client.fetch.return_value.set_result(mock_response)

    result = await handler.oauth2_request(
        "https://api.example.com/resource",
        access_token="token123",
        post_args={"name": "test"},
        extra="value",
    )

    # Verify that fetch was called with correct URL and method
    expected_url = "https://api.example.com/resource?access_token=token123&extra=value"
    mock_client.fetch.assert_awaited_once_with(
        expected_url,
        method="POST",
        body=urllib.parse.urlencode({"name": "test"}),
    )

    # Verify that the JSON body was decoded correctly
    assert result == {"ok": True, "data": {"id": 42}}
