import asyncio
import json
import urllib.parse

import pytest
from tornado import escape

# Import the mixin from the production module
from tornado.auth import GoogleOAuth2Mixin


class DummyHTTPClient:
    """A minimal HTTP client that records the request and returns a preset response."""

    def __init__(self, body: bytes):
        self.body = body
        self.last_request = None

    async def fetch(self, url, method=None, headers=None, body=None):
        self.last_request = {
            "url": url,
            "method": method,
            "headers": headers,
            "body": body,
        }
        # Simulate a successful JSON response
        return type("Response", (), {"body": self.body})


class TestGoogleOAuth2Mixin:
    """Test suite for GoogleOAuth2Mixin.get_authenticated_user."""

    @pytest.fixture
    def mixin(self):
        """Return a subclass instance with overridden HTTP client."""
        class TestMixin(GoogleOAuth2Mixin):
            def __init__(self, settings):
                self.settings = settings

            def get_auth_http_client(self):
                # Return a dummy client that will be replaced in each test
                return DummyHTTPClient(b'{}')

        return TestMixin({"google_oauth": {"key": "dummy_key", "secret": "dummy_secret"}})

    @pytest.mark.asyncio
    async def test_uses_settings_when_client_id_missing(self, mixin):
        """When client_id is None, the mixin should use the key from settings."""
        # Replace the HTTP client with one that records the request
        mixin.get_auth_http_client = lambda: DummyHTTPClient(b'{}')
        # Call with client_id=None to trigger lookup
        await mixin.get_authenticated_user(
            redirect_uri="https://example.com/callback",
            code="authcode",
            client_id=None,
            client_secret="explicit_secret",
        )
        # Inspect the body sent in the request
        body = urllib.parse.parse_qs(mixin.get_auth_http_client().last_request["body"])
        assert body["client_id"][0] == "dummy_key"
        assert body["client_secret"][0] == "explicit_secret"

    @pytest.mark.asyncio
    async def test_body_contains_redirect_and_code(self, mixin):
        """The request body must contain the redirect_uri and code parameters."""
        mixin.get_auth_http_client = lambda: DummyHTTPClient(b'{}')
        await mixin.get_authenticated_user(
            redirect_uri="https://example.com/callback",
            code="authcode",
            client_id="explicit_key",
            client_secret="explicit_secret",
        )
        body = urllib.parse.parse_qs(mixin.get_auth_http_client().last_request["body"])
        assert body["redirect_uri"][0] == "https://example.com/callback"
        assert body["code"][0] == "authcode"

    @pytest.mark.asyncio
    async def test_returns_decoded_json(self, mixin):
        """The method should return a dict decoded from the HTTP response body."""
        # Prepare a JSON payload to be returned by the dummy client
        payload = {"access_token": "token123", "expires_in": 3600}
        mixin.get_auth_http_client = lambda: DummyHTTPClient(json.dumps(payload).encode())
        result = await mixin.get_authenticated_user(
            redirect_uri="https://example.com/callback",
            code="authcode",
            client_id="explicit_key",
            client_secret="explicit_secret",
        )
        assert isinstance(result, dict)
        assert result == payload
