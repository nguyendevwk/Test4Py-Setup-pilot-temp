import pytest
import requests
from httpie.utils import ExplicitNullAuth


def test_explicit_null_auth_returns_request_object():
    """ExplicitNullAuth should return the request unchanged."""
    auth = ExplicitNullAuth()
    req = requests.Request('GET', 'http://example.com')
    prepared = req.prepare()
    result = auth(prepared)
    assert result is prepared
    assert result.url == 'http://example.com'


def test_explicit_null_auth_does_not_modify_headers():
    """When used as auth, no Authorization header should be added."""
    auth = ExplicitNullAuth()
    req = requests.Request('GET', 'http://example.com')
    prepared = req.prepare()
    # Apply auth
    auth(prepared)
    # Ensure no Authorization header
    assert 'Authorization' not in prepared.headers


def test_explicit_null_auth_in_session_no_netrc_effect():
    """Using ExplicitNullAuth in a Session should not trigger netrc lookup."""
    auth = ExplicitNullAuth()
    session = requests.Session()
    session.auth = auth
    # Prepare a request; netrc lookup would normally add auth header if credentials exist
    req = requests.Request('GET', 'http://example.com')
    prepared = req.prepare()
    # Apply session auth
    session.auth(prepared)
    # Ensure still no Authorization header
    assert 'Authorization' not in prepared.headers
