import pytest
import requests
from httpie.utils import ExplicitNullAuth

def test_explicit_null_auth_returns_same_request():
    """ExplicitNullAuth should return the request unchanged."""
    req = requests.Request('GET', 'https://example.com')
    prepared = req.prepare()
    auth = ExplicitNullAuth()
    result = auth(prepared)
    assert result is prepared, "Auth should return the same request object"

def test_explicit_null_auth_does_not_add_auth_header():
    """ExplicitNullAuth should not add any Authorization header."""
    req = requests.Request('GET', 'https://example.com')
    prepared = req.prepare()
    auth = ExplicitNullAuth()
    auth(prepared)
    assert 'Authorization' not in prepared.headers, "No Authorization header should be added"

def test_explicit_null_auth_with_missing_request_raises_type_error():
    """Calling ExplicitNullAuth with None should raise a TypeError."""
    auth = ExplicitNullAuth()
    with pytest.raises(TypeError):
        auth(None)
