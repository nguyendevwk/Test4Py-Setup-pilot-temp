import asyncio
import json
import urllib.parse

import pytest
from tornado import escape
from tornado.httputil import url_concat
from tornado.util import unicode_type

# Dummy mixin subclass for testing
class DummyOAuthHandler:
    _OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    _OAUTH_ACCESS_TOKEN_URL = "https://example.com/token"

    def __init__(self):
        self.redirected_to = None

    def redirect(self, url: str) -> None:
        self.redirected_to = url

    def get_auth_http_client(self):
        return DummyHTTPClient()


class DummyHTTPClient:
    async def fetch(self, url, method="GET", body=None):
        # Return a simple JSON body for testing
        class Response:
            body = json.dumps({"ok": True, "url": url, "body": body}).encode()
        return Response()


# Import the mixin after defining DummyOAuthHandler
from tornado.auth import OAuth2Mixin

# Attach mixin to dummy handler
class TestHandler(DummyOAuthHandler, OAuth2Mixin):
    pass


@pytest.mark.asyncio
async def test_authorize_redirect_builds_correct_url():
    handler = TestHandler()
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        scope=["email", "profile"],
        response_type="token",
    )
    # Expected query string
    expected_query = urllib.parse.urlencode(
        {
            "response_type": "token",
            "redirect_uri": "https://myapp.com/callback",
            "client_id": "abc123",
            "scope": "email profile",
        }
    )
    assert handler.redirected_to == f"https://example.com/auth?{expected_query}"
    # Ensure redirect was called exactly once
    assert handler.redirected_to.startswith("https://example.com/auth")


def test_oauth_request_token_url_construction():
    handler = TestHandler()
    url = handler._oauth_request_token_url(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        client_secret="secret",
        code="code123",
        extra_params={"state": "xyz"},
    )
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    # All parameters should be present
    assert query["redirect_uri"] == ["https://myapp.com/callback"]
    assert query["client_id"] == ["abc123"]
    assert query["client_secret"] == ["secret"]
    assert query["code"] == ["code123"]
    assert query["state"] == ["xyz"]
    # URL should start with the token endpoint
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/token"


@pytest.mark.asyncio
async def test_oauth2_request_fetch_and_decode():
    handler = TestHandler()
    # Perform a GET request with access_token
    result = await handler.oauth2_request(
        "https://api.example.com/data",
        access_token="token123",
        foo="bar",
    )
    # The dummy client returns JSON containing the URL and body
    assert isinstance(result, dict)
    assert result["ok"] is True
    # URL should include access_token and foo as query params
    parsed = urllib.parse.urlparse(result["url"])
    query = urllib.parse.parse_qs(parsed.query)
    assert query["access_token"] == ["token123"]
    assert query["foo"] == ["bar"]
    # Body should be None for GET
    assert result["body"] is None

    # Perform a POST request with body
    post_result = await handler.oauth2_request(
        "https://api.example.com/post",
        post_args={"msg": "hello"},
    )
    assert isinstance(post_result, dict)
    assert post_result["ok"] is True
    # Body should be URL-encoded form data
    assert post_result["body"] == "msg=hello"
