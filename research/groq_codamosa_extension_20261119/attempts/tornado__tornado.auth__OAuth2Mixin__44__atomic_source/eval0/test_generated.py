import pytest
import tornado.web
import tornado.auth
import tornado.httpclient
import urllib.parse

class DummyHandler(tornado.web.RequestHandler, tornado.auth.OAuth2Mixin):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.redirected_to = None

    def redirect(self, url, permanent=False, **kwargs):
        self.redirected_to = url

@pytest.fixture
def dummy_handler():
    app = tornado.web.Application()
    request = tornado.web.RequestHandler._RequestHandler__init__  # dummy
    return DummyHandler(app, None)

def test_authorize_redirect_builds_correct_url(dummy_handler):
    dummy_handler._OAUTH_AUTHORIZE_URL = "https://example.com/auth"
    dummy_handler.authorize_redirect(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        scope=["email", "profile"],
        response_type="token",
    )
    parsed = urllib.parse.urlparse(dummy_handler.redirected_to)
    query = urllib.parse.parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "example.com"
    assert parsed.path == "/auth"
    assert query["response_type"] == ["token"]
    assert query["redirect_uri"] == ["https://myapp.com/callback"]
    assert query["client_id"] == ["abc123"]
    assert query["scope"] == ["email profile"]

def test_oauth_request_token_url_construction(dummy_handler):
    dummy_handler._OAUTH_ACCESS_TOKEN_URL = "https://api.example.com/token"
    url = dummy_handler._oauth_request_token_url(
        redirect_uri="https://myapp.com/callback",
        client_id="abc123",
        client_secret="secret",
        code="code123",
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
    assert query["code"] == ["code123"]
    assert query["grant_type"] == ["authorization_code"]

def test_get_auth_http_client_returns_async_http_client(dummy_handler):
    client = dummy_handler.get_auth_http_client()
    assert isinstance(client, tornado.httpclient.AsyncHTTPClient)
