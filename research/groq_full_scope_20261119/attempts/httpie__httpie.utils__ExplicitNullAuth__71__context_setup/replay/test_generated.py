import pytest
import requests
from httpie.utils import ExplicitNullAuth

class DummyRequest:
    """Simple stand‑in for a requests.Request object."""
    def __init__(self, headers=None, data=None):
        self.headers = headers or {}
        self.data = data

def test_explicit_null_auth_is_auth_base():
    """ExplicitNullAuth should be a subclass of requests.auth.AuthBase."""
    auth = ExplicitNullAuth()
    assert isinstance(auth, requests.auth.AuthBase)

def test_call_returns_same_request_object(tmp_path):
    """Calling the auth on a request should return the exact same object."""
    auth = ExplicitNullAuth()
    req = DummyRequest(headers={"X-Test": "value"}, data="payload")
    result = auth(req)
    assert result is req
    assert result.headers == {"X-Test": "value"}
    assert result.data == "payload"

def test_call_does_not_modify_request(tmp_path):
    """The auth should not alter the request's attributes."""
    auth = ExplicitNullAuth()
    original_headers = {"Content-Type": "application/json"}
    req = DummyRequest(headers=original_headers.copy(), data='{"key":"value"}')
    auth(req)
    # Ensure headers remain unchanged
    assert req.headers == original_headers
    # Ensure data remains unchanged
    assert req.data == '{"key":"value"}'
