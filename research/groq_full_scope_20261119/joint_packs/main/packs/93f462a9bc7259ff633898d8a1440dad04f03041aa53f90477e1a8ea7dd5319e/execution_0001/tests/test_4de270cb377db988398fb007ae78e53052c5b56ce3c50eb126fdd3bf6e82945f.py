import pytest
import requests
from httpie.utils import ExplicitNullAuth

def test_explicit_null_auth_returns_same_request():
    """ExplicitNullAuth should return the request unchanged."""
    req = requests.Request(method="GET", url="http://example.com")
    prepared = req.prepare()
    auth = ExplicitNullAuth()
    result = auth(prepared)
    assert result is prepared, "Auth should return the same request object"

def test_explicit_null_auth_does_not_modify_headers():
    """Auth should not add or modify any headers."""
    req = requests.Request(method="GET", url="http://example.com")
    prepared = req.prepare()
    original_headers = prepared.headers.copy()
    auth = ExplicitNullAuth()
    auth(prepared)
    assert prepared.headers == original_headers, "Headers should remain unchanged"

def test_explicit_null_auth_in_request_preparation():
    """When used as auth in a Request, no Authorization header should be added."""
    req = requests.Request(method="GET", url="http://example.com", auth=ExplicitNullAuth())
    prepared = req.prepare()
    assert "Authorization" not in prepared.headers, "ExplicitNullAuth should not set Authorization header"
