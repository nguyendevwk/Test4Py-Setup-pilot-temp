import asyncio
import urllib.parse
import json
import pytest
from tornado.web import RequestHandler
from tornado.auth import OAuth2Mixin
from tornado.httpclient import AsyncHTTPClient, HTTPResponse
from tornado import escape

# ---------- Helper classes ----------

class DummyHandler(RequestHandler, OAuth2Mixin):
    """A minimal RequestHandler that records the last redirect URL."""
    def __init__(self, application=None, request=None, **kwargs):
        super().__init__(application, request, **kwargs)
        self.redirected_to = None

    def redirect(self, url, *args, **kwargs):
        self.redirected_to = url

    def get_auth_http_client(self):
        """Return a fake HTTP client that returns a predetermined response."""
        return FakeHTTPClient()

class FakeHTTPClient:
    """A fake AsyncHTTPClient that returns a fixed JSON response."""
    async def fetch(self, url, method="GET", body=None):
        # Return a simple JSON body containing the URL and method for inspection
        body_dict = {"url": url, "method": method, "body": body}
        return HTTPResponse(
            request=None,
            code=200,
            headers={},
            buffer=bytes(json.dumps(body_dict), "utf-8"),
            request_time=0.0,
        )

# ---------- Tests ----------

def test_authorize_redirect_builds_correct_url():
    """authorize_redirect should construct the correct redirect URL."""
    handler = DummyHandler()
    handler._OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        scope=["email", "profile"],
        response_type="token",
        extra_params={"state": "xyz"},
    )
    parsed = urllib.parse.urlparse(handler.redirected_to)
    query = urllib.parse.parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/auth"
    assert query["response_type"] == ["token"]
    assert query["redirect_uri"] == ["https://myapp.com/callback"]
    assert query["client_id"] == ["abc123"]
    assert query["scope"] == ["email profile"]
    assert query["state"] == ["xyz"]

def test_oauth_request_token_url_construction():
    """_oauth_request_token_url should correctly assemble query parameters."""
    handler = DummyHandler()
    handler._OAUTH_ACCESS_TOKEN_URL = "https://api.example.com/token"
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
    assert parsed.netloc == "api.example.com"
    assert parsed.path == "/token"
    assert query["redirect_uri"] == ["https://myapp.com/callback"]
    assert query["client_id"] == ["abc123"]
    assert query["client_secret"] == ["secret"]
    assert query["code"] == ["authcode"]
    assert query["grant_type"] == ["authorization_code"]

@pytest.mark.asyncio
async def test_oauth2_request_uses_access_token_and_post_args():
    """oauth2_request should append access_token and send POST body correctly."""
    handler = DummyHandler()
    handler._OAUTH_ACCESS_TOKEN_URL = "https://api.example.com/resource"
    # Perform a POST request with access_token and post_args
    result = await handler.oauth2_request(
        url="https://api.example.com/resource",
        access_token="mytoken",
        post_args={"foo": "bar"},
        extra="value",
    )
    # The fake client returns the URL, method, and body in JSON
    assert result["method"] == "POST"
    # URL should contain access_token and extra as query parameters
    parsed = urllib.parse.urlparse(result["url"])
    query = urllib.parse.parse_qs(parsed.query)
    assert query["access_token"] == ["mytoken"]
    assert query["extra"] == ["value"]
    # Body should be URL-encoded post_args
    assert result["body"] == urllib.parse.urlencode({"foo": "bar"})
