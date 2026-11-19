import pytest
from http.cookies import SimpleCookie
from requests.cookies import RequestsCookieJar
from httpie.sessions import materialize_cookies, materialize_cookie, KEPT_COOKIE_OPTIONS

def test_materialize_cookies_basic():
    jar = RequestsCookieJar()
    jar.set('foo', 'bar', path='/', domain='example.com', secure=True, expires=1234567890)
    result = materialize_cookies(jar)
    assert isinstance(result, list)
    assert len(result) == 1
    cookie_dict = result[0]
    for key in KEPT_COOKIE_OPTIONS:
        assert key in cookie_dict
    assert cookie_dict['name'] == 'foo'
    assert cookie_dict['value'] == 'bar'
    assert cookie_dict['domain'] == 'example.com'
    assert cookie_dict['secure'] is True
    assert cookie_dict['expires'] == 1234567890
    assert cookie_dict['path'] == '/'

def test_materialize_cookies_domain_none_explicit():
    jar = RequestsCookieJar()
    # Simulate explicit None domain by setting _rest flag
    cookie = jar.set('baz', 'qux', domain='', path='/', secure=False, expires=None)
    # Access the underlying Cookie object
    cookie_obj = next(iter(jar))
    cookie_obj._rest['is_explicit_none'] = True
    result = materialize_cookies(jar)
    assert result[0]['domain'] is None

def test_materialize_cookies_multiple_and_order():
    jar = RequestsCookieJar()
    jar.set('a', '1', domain='a.com')
    jar.set('b', '2', domain='b.com')
    jar.set('c', '3', domain='c.com')
    result = materialize_cookies(jar)
    names = [c['name'] for c in result]
    assert names == ['a', 'b', 'c']
    # Ensure each cookie dict contains only the kept options
    for c in result:
        assert set(c.keys()) == set(KEPT_COOKIE_OPTIONS)
