import pytest
import warnings
from urllib.parse import urlparse, parse_qs
from tornado.auth import OAuth2Mixin
from tornado.web import RequestHandler
from tornado import httpclient, escape
from tornado.httputil import url_concat
from tornado.util import unicode_type

# Dummy handler that mixes in OAuth2Mixin and implements redirect
class DummyHandler(RequestHandler, OAuth2Mixin):
    def __init__(self, *args, **kwargs):
        # RequestHandler requires a request argument; we pass None for tests
        super().__init__(None, None)
        self.redirected_to = None

    def redirect(self, url, *args, **kwargs):
        self.redirected_to = url

# Helper to create a minimal AsyncHTTPClient that returns a preset response
class DummyHTTPClient(httpclient.AsyncHTTPClient):
    def __init__(self, body):
        super().__init__()
        self._body = body

    async def fetch(self, url, method="GET", body=None):
        class DummyResponse:
            def __init__(self, body):
                self.body = body
        return DummyResponse(self._body)

@pytest.fixture
def handler():
    h = DummyHandler()
    h._OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    h._OAUTH_ACCESS_TOKEN_URL = "https://example.com/token"
    return h

def test_authorize_redirect_builds_correct_url(handler):
    handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        scope=["email", "profile"],
        response_type="token",
        extra_params={"state": "xyz"}
    )
    parsed = urlparse(handler.redirected_to)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/auth"
    qs = parse_qs(parsed.query)
    assert qs["response_type"] == ["token"]
    assert qs["redirect_uri"] == ["https://myapp.com/callback"]
    assert qs["client_id"] == ["abc123"]
    assert qs["scope"] == ["email profile"]
    assert qs["state"] == ["xyz"]

def test_oauth_request_token_url_includes_all_params(handler):
    url = handler._oauth_request_token_url(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        client_secret="secret",
        code="code123",
        extra_params={"grant_type": "authorization_code"}
    )
    parsed = urlparse(url)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/token"
    qs = parse_qs(parsed.query)
    assert qs["redirect_uri"] == ["https://myapp.com/callback"]
    assert qs["client_id"] == ["abc123"]
    assert qs["client_secret"] == ["secret"]
    assert qs["code"] == ["code123"]
    assert qs["grant_type"] == ["authorization_code"]

def test_oauth2_request_fetches_and_parses_json(handler):
    # Prepare a dummy HTTP client that returns JSON
    response_body = escape.json_encode({"access_token": "token123", "expires_in": 3600})
    handler.get_auth_http_client = lambda: DummyHTTPClient(response_body)

    # Call oauth2_request with a GET
    result = pytest.run_async(handler.oauth2_request(
        url="https://api.example.com/data",
        access_token="token123",
        param="value"
    ))
    assert isinstance(result, dict)
    assert result["access_token"] == "token123"
    assert result["expires_in"] == 3600

    # Call oauth2_request with a POST
    result_post = pytest.run_async(handler.oauth2_request(
        url="https://api.example.com/data",
        post_args={"key": "value"},
        access_token="token123"
    ))
    assert isinstance(result_post, dict)
    assert result_post["access_token"] == "token123"
