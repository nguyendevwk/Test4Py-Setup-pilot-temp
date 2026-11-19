import asyncio
import json
import urllib.parse
import pytest
from tornado import escape
from tornado.web import RequestHandler
from tornado.auth import GoogleOAuth2Mixin

class DummyHandler(RequestHandler, GoogleOAuth2Mixin):
    def initialize(self, settings):
        self.settings = settings

    def get_auth_http_client(self):
        return self.http_client

class DummyHttpClient:
    def __init__(self):
        self.last_fetch = None

    async def fetch(self, url, method=None, headers=None, body=None):
        self.last_fetch = {"url": url, "method": method, "headers": headers, "body": body}
        # Simulate a JSON response
        return type("Response", (), {"body": json.dumps({"access_token": "dummy_token"}).encode()})()

@pytest.mark.asyncio
async def test_get_google_oauth_settings_returns_dict():
    settings = {"google_oauth": {"key": "client_id", "secret": "client_secret"}}
    handler = DummyHandler(settings=settings)
    result = handler.get_google_oauth_settings()
    assert isinstance(result, dict)
    assert result["key"] == "client_id"
    assert result["secret"] == "client_secret"

@pytest.mark.asyncio
async def test_get_authenticated_user_uses_provided_credentials():
    settings = {"google_oauth": {"key": "unused", "secret": "unused"}}
    handler = DummyHandler(settings=settings)
    handler.http_client = DummyHttpClient()
    redirect_uri = "https://example.com/callback"
    code = "authcode"
    client_id = "provided_id"
    client_secret = "provided_secret"

    user = await handler.get_authenticated_user(
        redirect_uri=redirect_uri,
        code=code,
        client_id=client_id,
        client_secret=client_secret,
    )

    # Verify that the HTTP client was called with correct parameters
    fetch_args = handler.http_client.last_fetch
    assert fetch_args["url"] == handler._OAUTH_ACCESS_TOKEN_URL
    assert fetch_args["method"] == "POST"
    assert fetch_args["headers"] == {"Content-Type": "application/x-www-form-urlencoded"}
    body_dict = dict(urllib.parse.parse_qsl(fetch_args["body"]))
    assert body_dict["redirect_uri"] == redirect_uri
    assert body_dict["code"] == code
    assert body_dict["client_id"] == client_id
    assert body_dict["client_secret"] == client_secret
    assert body_dict["grant_type"] == "authorization_code"

    # Verify that the returned user dict contains the expected access token
    assert user == {"access_token": "dummy_token"}

@pytest.mark.asyncio
async def test_get_authenticated_user_uses_settings_when_none():
    settings = {"google_oauth": {"key": "settings_id", "secret": "settings_secret"}}
    handler = DummyHandler(settings=settings)
    handler.http_client = DummyHttpClient()
    redirect_uri = "https://example.com/callback"
    code = "authcode"

    user = await handler.get_authenticated_user(
        redirect_uri=redirect_uri,
        code=code,
        client_id=None,
        client_secret=None,
    )

    fetch_args = handler.http_client.last_fetch
    body_dict = dict(urllib.parse.parse_qsl(fetch_args["body"]))
    assert body_dict["client_id"] == "settings_id"
    assert body_dict["client_secret"] == "settings_secret"
    assert user == {"access_token": "dummy_token"}
