import pytest
import asyncio
from tornado.web import RequestHandler
from tornado.auth import GoogleOAuth2Mixin
from tornado.util import unicode_type

class DummyHandler(RequestHandler, GoogleOAuth2Mixin):
    def initialize(self, settings):
        self.settings = settings

    def get_auth_http_client(self):
        # Override to avoid real network calls
        class DummyClient:
            async def fetch(self, url, method, headers, body):
                raise RuntimeError("Network not allowed in tests")
        return DummyClient()

def test_get_google_oauth_settings_returns_expected_dict():
    settings = {"google_oauth": {"key": "client_id", "secret": "client_secret"}}
    handler = DummyHandler(application=None, request=None, **settings)
    result = handler.get_google_oauth_settings()
    assert isinstance(result, dict)
    assert result["key"] == "client_id"
    assert result["secret"] == "client_secret"

def test_get_authenticated_user_uses_settings_when_none_provided():
    settings = {"google_oauth": {"key": "client_id", "secret": "client_secret"}}
    handler = DummyHandler(application=None, request=None, **settings)
    async def run():
        with pytest.raises(RuntimeError, match="Network not allowed in tests"):
            await handler.get_authenticated_user(
                redirect_uri="https://example.com/callback",
                code="dummy_code",
            )
    asyncio.run(run())

def test_get_authenticated_user_raises_when_settings_missing():
    settings = {"google_oauth": {"key": "client_id"}}  # missing 'secret'
    handler = DummyHandler(application=None, request=None, **settings)
    with pytest.raises(KeyError):
        handler.get_google_oauth_settings()["secret"]
