import asyncio
import json
import pytest
from tornado.web import RequestHandler
from tornado.auth import GoogleOAuth2Mixin
from tornado import escape

class DummyHandler(RequestHandler, GoogleOAuth2Mixin):
    def initialize(self, **settings):
        self.settings.update(settings)

    def get_auth_http_client(self):
        # Return a dummy http client that records the request
        return DummyHTTPClient()

class DummyHTTPClient:
    def __init__(self):
        self.last_request = None

    async def fetch(self, url, method=None, headers=None, body=None):
        self.last_request = {
            "url": url,
            "method": method,
            "headers": headers,
            "body": body,
        }
        # Simulate a successful token response
        return DummyResponse(b'{"access_token":"dummy_token","expires_in":3600}')

class DummyResponse:
    def __init__(self, body):
        self.body = body

@pytest.mark.asyncio
async def test_get_google_oauth_settings_returns_handler_settings():
    handler = DummyHandler()
    handler.settings["google_oauth"] = {"key": "client_id", "secret": "client_secret"}
    settings = handler.get_google_oauth_settings()
    assert isinstance(settings, dict)
    assert settings["key"] == "client_id"
    assert settings["secret"] == "client_secret"

@pytest.mark.asyncio
async def test_get_authenticated_user_uses_settings_when_missing_client_id_and_secret():
    handler = DummyHandler()
    handler.settings["google_oauth"] = {"key": "client_id", "secret": "client_secret"}
    # Call with None to trigger fallback to settings
    result = await handler.get_authenticated_user(
        redirect_uri="https://example.com/callback",
        code="dummy_code",
        client_id=None,
        client_secret=None,
    )
    # Verify that the dummy http client was called with correct body
    http = handler.get_auth_http_client()
    body = http.last_request["body"]
    parsed = dict(urllib.parse.parse_qsl(body))
    assert parsed["client_id"] == "client_id"
    assert parsed["client_secret"] == "client_secret"
    assert parsed["redirect_uri"] == "https://example.com/callback"
    assert parsed["code"] == "dummy_code"
    assert parsed["grant_type"] == "authorization_code"
    # Verify that the returned token matches the dummy response
    assert result["access_token"] == "dummy_token"
    assert result["expires_in"] == 3600

@pytest.mark.asyncio
async def test_get_authenticated_user_overrides_settings_with_provided_client_id_and_secret():
    handler = DummyHandler()
    handler.settings["google_oauth"] = {"key": "client_id", "secret": "client_secret"}
    # Provide explicit client_id and client_secret
    result = await handler.get_authenticated_user(
        redirect_uri="https://example.com/callback",
        code="dummy_code",
        client_id="explicit_id",
        client_secret="explicit_secret",
    )
    http = handler.get_auth_http_client()
    body = http.last_request["body"]
    parsed = dict(urllib.parse.parse_qsl(body))
    assert parsed["client_id"] == "explicit_id"
    assert parsed["client_secret"] == "explicit_secret"
    assert result["access_token"] == "dummy_token"
