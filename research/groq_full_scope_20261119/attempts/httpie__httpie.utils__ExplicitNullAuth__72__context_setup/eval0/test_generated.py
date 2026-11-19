import pytest
import requests
from httpie.utils import ExplicitNullAuth

def test_explicit_null_auth_returns_same_request(tmp_path):
    # Create a simple request
    req = requests.Request('GET', 'http://example.com')
    prepped = req.prepare()
    # Apply ExplicitNullAuth
    auth = ExplicitNullAuth()
    result = auth(prepped)
    # The returned object should be the same instance
    assert result is prepped
    # No auth header should be added
    assert 'Authorization' not in result.headers

def test_explicit_null_auth_does_not_modify_headers(tmp_path):
    # Prepare a request with an existing Authorization header
    req = requests.Request('GET', 'http://example.com')
    req.headers['Authorization'] = 'Bearer token'
    prepped = req.prepare()
    # Apply ExplicitNullAuth
    auth = ExplicitNullAuth()
    result = auth(prepped)
    # The Authorization header should remain unchanged
    assert result.headers['Authorization'] == 'Bearer token'
    # The request object should still be the same
    assert result is prepped

def test_explicit_null_auth_is_callable_and_raises_on_invalid_input():
    auth = ExplicitNullAuth()
    # ExplicitNullAuth should be callable
    assert callable(auth)
    # Calling with None should raise a TypeError because requests expects a PreparedRequest
    with pytest.raises(TypeError):
        auth(None)
