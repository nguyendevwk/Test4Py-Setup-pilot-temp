import time
import pytest
from httpie.utils import get_expired_cookies, _max_age_to_expires, split_cookies

def test_expired_and_non_expired_cookies():
    # Cookie string with one expired and one non‑expired cookie
    now = time.time()
    expired_cookie = f"session=abc; Expires={time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(now - 10))}"
    non_expired_cookie = f"token=xyz; Expires={time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(now + 1000))}"
    cookies_str = f"{expired_cookie}, {non_expired_cookie}"
    result = get_expired_cookies(cookies_str, now=now)
    assert len(result) == 1
    assert result[0]['name'] == 'session'
    assert result[0]['path'] == '/'  # default path

def test_max_age_conversion_to_expires():
    # Cookie with max-age but no Expires attribute
    now = time.time()
    cookie_str = "id=123; Max-Age=5"
    # split_cookies returns list of cookie strings
    attr_sets = split_cookies(cookie_str)
    # parse_ns_headers expects list of cookie strings
    from http.cookiejar import parse_ns_headers
    attrs = parse_ns_headers(attr_sets)
    cookies = [dict(a[1:], name=a[0][0]) for a in attrs]
    _max_age_to_expires(cookies=cookies, now=now)
    # After conversion, expires should be now + 5
    expires = cookies[0].get('expires')
    assert expires is not None
    assert abs(expires - (now + 5)) < 1e-6

def test_empty_and_invalid_cookie_strings():
    # Empty string should yield no expired cookies
    assert get_expired_cookies("") == []

    # Malformed cookie string that cannot be parsed should not raise
    malformed = "badcookie"
    result = get_expired_cookies(malformed)
    # Since no Expires attribute, it should not be considered expired
    assert result == []
