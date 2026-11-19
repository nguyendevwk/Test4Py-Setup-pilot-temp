import pytest
import urllib.parse
from tornado import escape
from tornado.auth import GoogleOAuth2Mixin
from tornado.web import RequestHandler
from typing import Dict, Any


class DummyHTTPClient:
    """A dummy HTTP client that records the request body and returns a fake response."""
    def __init__(self):
        self.last_body = None

    async def fetch(self, url, method=None, headers=None, body=None):
        self.last_body = body
        # Return a minimal fake response with a JSON body
        class Response:
            body = b'{"access_token":"dummy_token"}'
        return Response()


class DummyHandler(GoogleOAuth2Mixin, RequestHandler):
    """A minimal RequestHandler that supplies settings and a dummy HTTP client."""
    def __init__(self, settings: Dict[str, Any]):
        self.settings = settings

    def get_auth_http_client(self):
        return DummyHTTPClient()


@pytest.mark.asyncio
async def test_get_authenticated_user_uses_settings_and_returns_token():
    """Verify that the mixin uses the client id/secret from settings and returns the
    access token from the HTTP response."""
    handler = DummyHandler(
        {"google_oauth": {"key": "client_id_123", "secret": "secret_abc"}}
    )
    result = await handler.get_authenticated_user(
        redirect_uri="https://example.com/callback",
        code="auth_code_xyz",
    )
    # The dummy client returns a JSON with access_token
    assert result == {"access_token": "dummy_token"}
    # Inspect the body sent to the dummy HTTP client
    body = urllib.parse.parse_qs(handler.get_auth_http_client().last_body.decode())
    assert body["redirect_uri"] == ["https://example.com/callback"]
    assert body["code"] == ["auth_code_xyz"]
    assert body["client_id"] == ["client_id_123"]
    assert body["client_secret"] == ["secret_abc"]
    assert body["grant_type"] == ["authorization_code"]


@pytest.mark.asyncio
async def test_get_authenticated_user_allows_explicit_client_credentials():
    """Verify that passing explicit client_id and client_secret overrides the settings."""
    handler = DummyHandler(
        {"google_oauth": {"key": "ignored_id", "secret": "ignored_secret"}}
    )
    result = await handler.get_authenticated_user(
        redirect_uri="https://example.com/callback",
        code="code_456",
        client_id="explicit_id",
        client_secret="explicit_secret",
    )
    assert result == {"access_token": "dummy_token"}
    body = urllib.parse.parse_qs(handler.get_auth_http_client().last_body.decode())
    assert body["client_id"] == ["explicit_id"]
    assert body["client_secret"] == ["explicit_secret"]


def test_get_google_oauth_settings_missing_raises_key_error():
    """Verify that missing google_oauth settings raise a KeyError."""
    handler = DummyHandler(settings={})
    with pytest.raises(KeyError):
        handler.get_google_oauth_settings()
