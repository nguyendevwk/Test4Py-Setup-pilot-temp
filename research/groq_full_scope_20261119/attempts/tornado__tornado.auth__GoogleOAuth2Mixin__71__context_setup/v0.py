import asyncio
import urllib.parse
import json
import pytest
from tornado.auth import GoogleOAuth2Mixin
from tornado.web import RequestHandler
from tornado.util import unicode_type

# Helper handler that supplies settings and overrides HTTP client
class DummyHandler(RequestHandler, GoogleOAuth2Mixin):
    def initialize(self, settings):
        self.settings = settings

    def get_auth_http_client(self):
        # Return a dummy client that records the request
        return DummyHttpClient(self._recorded_request)

    def _recorded_request(self, url, method, headers, body):
        self._recorded_request = {
            "url": url,
            "method": method,
            "headers": headers,
            "body": body,
        }

class DummyHttpClient:
    def __init__(self, record_callback):
        self._record_callback = record_callback

    async def fetch(self, url, method=None, headers=None, body=None):
        # Record the request and raise to avoid network
        self._record_callback(url, method, headers, body)
        raise RuntimeError("Dummy fetch called")

@pytest.mark.asyncio
async def test_get_google_oauth_settings_returns_dict(tmp_path):
    settings = {"google_oauth": {"key": "client-id", "secret": "client-secret"}}
    handler = DummyHandler(settings=settings)
    result = handler.get_google_oauth_settings()
    assert isinstance(result, dict)
    assert result["key"] == "client-id"
    assert result["secret"] == "client-secret"

@pytest.mark.asyncio
async def test_get_authenticated_user_uses_settings_when_none(tmp_path):
    settings = {"google_oauth": {"key": "client-id", "secret": "client-secret"}}
    handler = DummyHandler(settings=settings)
    # The dummy fetch will raise; we only care that the body contains the settings
    with pytest.raises(RuntimeError, match="Dummy fetch called"):
        await handler.get_authenticated_user(
            redirect_uri="https://example.com/callback",
            code="dummy-code",
        )
    recorded = handler._recorded_request
    body_dict = urllib.parse.parse_qs(recorded["body"])
    assert body_dict["client_id"] == ["client-id"]
    assert body_dict["client_secret"] == ["client-secret"]
    assert body_dict["redirect_uri"] == ["https://example.com/callback"]
    assert body_dict["code"] == ["dummy-code"]
    assert body_dict["grant_type"] == ["authorization_code"]

@pytest.mark.asyncio
async def test_get_authenticated_user_raises_keyerror_when_settings_missing(tmp_path):
    # No google_oauth key in settings
    handler = DummyHandler(settings={})
    with pytest.raises(KeyError):
        handler.get_google_oauth_settings()
