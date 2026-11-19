import pytest
from http.cookiejar import Cookie
from httpie.sessions import materialize_cookie, KEPT_COOKIE_OPTIONS

def test_materialize_cookie_basic_attributes():
    # Create a cookie with all standard attributes
    cookie = Cookie(
        version=0,
        name='sessionid',
        value='abc123',
        port=None,
        port_specified=False,
        domain='example.com',
        domain_specified=True,
        domain_initial_dot=False,
        path='/',
        path_specified=True,
        secure=False,
        expires=1700000000,
        discard=False,
        comment=None,
        comment_url=None,
        rest={},
        rfc2109=False
    )
    result = materialize_cookie(cookie)
    # Assert that all kept options are present and correctly copied
    for opt in KEPT_COOKIE_OPTIONS:
        assert opt in result
        assert result[opt] == getattr(cookie, opt)
    # Ensure no extra keys are present
    assert set(result.keys()) == set(KEPT_COOKIE_OPTIONS)

def test_materialize_cookie_explicit_none_domain():
    # Cookie with explicit None domain and empty domain string
    cookie = Cookie(
        version=0,
        name='token',
        value='xyz',
        port=None,
        port_specified=False,
        domain='',
        domain_specified=True,
        domain_initial_dot=False,
        path='/',
        path_specified=True,
        secure=True,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest={'is_explicit_none': True},
        rfc2109=False
    )
    result = materialize_cookie(cookie)
    # Domain should be converted to None because of explicit_none flag
    assert result['domain'] is None
    # Other attributes remain unchanged
    assert result['secure'] is True
    assert result['name'] == 'token'

def test_materialize_cookie_missing_rest_key_raises():
    # Cookie missing the 'rest' attribute should raise AttributeError
    # Simulate by creating a Cookie with rest=None
    cookie = Cookie(
        version=0,
        name='id',
        value='123',
        port=None,
        port_specified=False,
        domain='example.com',
        domain_specified=True,
        domain_initial_dot=False,
        path='/',
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None,
        rfc2109=False
    )
    # materialize_cookie accesses cookie._rest; if rest is None, AttributeError occurs
    with pytest.raises(AttributeError):
        materialize_cookie(cookie)
