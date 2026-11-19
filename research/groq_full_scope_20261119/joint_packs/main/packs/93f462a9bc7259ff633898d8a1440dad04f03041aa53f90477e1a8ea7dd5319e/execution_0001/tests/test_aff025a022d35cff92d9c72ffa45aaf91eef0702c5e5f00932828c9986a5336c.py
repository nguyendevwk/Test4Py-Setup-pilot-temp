import time
import pytest
from httpie.utils import get_expired_cookies

def test_get_expired_cookies_returns_expired():
    # Cookie with expires 1 second in the past
    past = time.time() - 1
    cookie_str = f"sessionid=abc123; Expires={time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(past))}; Path=/; HttpOnly"
    expired = get_expired_cookies(cookie_str, now=time.time())
    assert len(expired) == 1
    assert expired[0]["name"] == "sessionid"
    assert expired[0]["path"] == "/"

def test_get_expired_cookies_boundary_expires_equals_now():
    # Cookie with expires exactly equal to now
    now = time.time()
    cookie_str = f"token=xyz; Expires={time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(now))}; Path=/"
    expired = get_expired_cookies(cookie_str, now=now)
    # Expires <= now should be considered expired
    assert len(expired) == 1
    assert expired[0]["name"] == "token"

def test_get_expired_cookies_invalid_cookie_returns_empty():
    # Malformed cookie string that parse_ns_headers cannot parse
    invalid_str = "this is not a valid cookie header"
    expired = get_expired_cookies(invalid_str, now=time.time())
    assert expired == []
