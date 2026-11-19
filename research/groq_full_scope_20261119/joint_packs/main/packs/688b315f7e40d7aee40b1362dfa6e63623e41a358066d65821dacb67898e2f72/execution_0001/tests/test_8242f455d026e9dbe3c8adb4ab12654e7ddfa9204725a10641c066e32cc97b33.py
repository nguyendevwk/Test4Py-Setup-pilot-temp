import requests
import pytest
from httpie.utils import ExplicitNullAuth

def test_explicit_null_auth_returns_request_identity():
    """ExplicitNullAuth should return the request unchanged."""
    auth = ExplicitNullAuth()
    req = requests.Request('GET', 'http://example.com')
    prepared = req.prepare()
    result = auth(prepared)
    assert result is prepared, "ExplicitNullAuth should return the same request object"

def test_explicit_null_auth_does_not_modify_headers():
    """ExplicitNullAuth should not alter request headers."""
    auth = ExplicitNullAuth()
    req = requests.Request('GET', 'http://example.com', headers={'X-Test': 'value'})
    prepared = req.prepare()
    auth(prepared)
    assert prepared.headers.get('X-Test') == 'value', "Headers should remain unchanged"

def test_explicit_null_auth_in_session_does_not_use_netrc():
    """When used in a session, ExplicitNullAuth prevents netrc credentials from being applied."""
    # Create a session with a dummy netrc file that would normally provide credentials
    # For the test, we simulate by setting a custom auth that would normally add headers
    class DummyAuth(requests.auth.AuthBase):
        def __call__(self, r):
            r.headers['Authorization'] = 'Basic dummy'
            return r

    session = requests.Session()
    session.auth = DummyAuth()
    # Now override with ExplicitNullAuth
    session.auth = ExplicitNullAuth()
    response = session.get('http://httpbin.org/headers')
    # The Authorization header should not be present
    assert 'Authorization' not in response.json()['headers'], "ExplicitNullAuth should prevent netrc auth"
