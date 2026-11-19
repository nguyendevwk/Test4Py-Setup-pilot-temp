import pytest
from http.cookies import SimpleCookie
from requests.cookies import RequestsCookieJar
from httpie.sessions import materialize_cookies

def test_materialize_cookies_basic():
    # Create a cookie jar with a single cookie
    jar = RequestsCookieJar()
    jar.set('sessionid', 'abc123', domain='example.com', path='/', secure=True, httponly=True)
    # Materialize the cookies
    result = materialize_cookies(jar)
    # Expect a single dict with the cookie attributes
    assert isinstance(result, list)
    assert len(result) == 1
    cookie_dict = result[0]
    assert cookie_dict['name'] == 'sessionid'
    assert cookie_dict['value'] == 'abc123'
    assert cookie_dict['domain'] == 'example.com'
    assert cookie_dict['path'] == '/'
    assert cookie_dict['secure'] is True
    assert cookie_dict['httpOnly'] is True
    # The 'expires' field should be None for a session cookie
    assert cookie_dict['expires'] is None

def test_materialize_cookies_multiple_and_order():
    # Create a cookie jar with multiple cookies
    jar = RequestsCookieJar()
    jar.set('a', '1', domain='foo.com', path='/')
    jar.set('b', '2', domain='bar.com', path='/')
    jar.set('c', '3', domain='baz.com', path='/')
    # Materialize the cookies
    result = materialize_cookies(jar)
    # The order of cookies in the result should match the order they were added
    names = [c['name'] for c in result]
    assert names == ['a', 'b', 'c']
    # Verify each cookie's value
    values = [c['value'] for c in result]
    assert values == ['1', '2', '3']

def test_materialize_cookies_empty_jar():
    # An empty cookie jar should produce an empty list
    jar = RequestsCookieJar()
    result = materialize_cookies(jar)
    assert result == []
