import pytest
from http.cookies import SimpleCookie
from http.cookiejar import Cookie, RequestsCookieJar
from httpie.sessions import materialize_cookies, materialize_cookie, KEPT_COOKIE_OPTIONS


def test_materialize_cookies_empty_jar_returns_empty_list():
    """When the cookie jar is empty, materialize_cookies should return an empty list."""
    jar = RequestsCookieJar()
    result = materialize_cookies(jar)
    assert result == []


def test_materialize_cookies_includes_expected_keys_and_values():
    """materialize_cookies should return a list of dicts containing only the KEPT_COOKIE_OPTIONS."""
    jar = RequestsCookieJar()
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
        rfc2109=False,
    )
    jar.set_cookie(cookie)
    result = materialize_cookies(jar)
    assert isinstance(result, list)
    assert len(result) == 1
    materialized = result[0]
    # All KEPT_COOKIE_OPTIONS must be present
    assert set(materialized.keys()) == set(KEPT_COOKIE_OPTIONS)
    # Values should match the original cookie
    assert materialized['name'] == 'sessionid'
    assert materialized['value'] == 'abc123'
    assert materialized['domain'] == 'example.com'
    assert materialized['path'] == '/'
    assert materialized['secure'] is False
    assert materialized['expires'] == 1700000000


def test_materialize_cookie_explicit_none_domain_becomes_none():
    """If a cookie has an empty domain and the rest flag 'is_explicit_none' is set,
    the domain should be converted to None."""
    cookie = Cookie(
        version=0,
        name='emptydomain',
        value='xyz',
        port=None,
        port_specified=False,
        domain='',
        domain_specified=True,
        domain_initial_dot=False,
        path='/',
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest={'is_explicit_none': True},
        rfc2109=False,
    )
    materialized = materialize_cookie(cookie)
    assert materialized['domain'] is None
    # Other fields remain unchanged
    assert materialized['name'] == 'emptydomain'
    assert materialized['value'] == 'xyz'
    assert materialized['path'] == '/'
    assert materialized['secure'] is False
    assert materialized['expires'] is None
