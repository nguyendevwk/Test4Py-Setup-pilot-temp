import pytest
from http.cookiejar import Cookie
from httpie.sessions import materialize_cookie

# Helper to create a Cookie with minimal required fields
def make_cookie(**kwargs):
    defaults = {
        'version': 0,
        'name': 'test',
        'value': 'value',
        'port': None,
        'port_specified': False,
        'domain': '',
        'domain_specified': False,
        'domain_initial_dot': False,
        'path': '/',
        'path_specified': True,
        'secure': False,
        'expires': None,
        'discard': False,
        'comment': None,
        'comment_url': None,
        'rest': {},
        'rfc2109': False,
    }
    defaults.update(kwargs)
    return Cookie(**defaults)

def test_materialize_cookie_preserves_attributes():
    """materialize_cookie should return a dict with all kept options unchanged."""
    cookie = make_cookie(name='foo', value='bar', domain='example.com', path='/path')
    result = materialize_cookie(cookie)
    assert result['name'] == 'foo'
    assert result['value'] == 'bar'
    assert result['domain'] == 'example.com'
    assert result['path'] == '/path'
    # Ensure no unexpected keys are present
    expected_keys = {'name', 'value', 'domain', 'path', 'secure', 'expires', 'discard',
                     'comment', 'comment_url', 'rest', 'rfc2109', 'port', 'port_specified',
                     'domain_specified', 'domain_initial_dot', 'path_specified', 'version'}
    assert set(result.keys()) == expected_keys

def test_materialize_cookie_explicit_none_domain():
    """If rest['is_explicit_none'] is True and domain is empty, domain becomes None."""
    cookie = make_cookie(domain='', rest={'is_explicit_none': True})
    result = materialize_cookie(cookie)
    assert result['domain'] is None

def test_materialize_cookie_no_explicit_none_no_change():
    """If rest['is_explicit_none'] is False or missing, domain remains unchanged."""
    cookie = make_cookie(domain='', rest={})
    result = materialize_cookie(cookie)
    assert result['domain'] == ''
