import time
import pytest
from httpie.utils import get_expired_cookies

def test_get_expired_cookies_returns_only_expired(tmp_path):
    # Create a cookie string with two cookies:
    # - one expired (expires 1 second ago)
    # - one still valid (expires 10 seconds in the future)
    now = time.time()
    expired_cookie = f"sessionid=abc123; Expires={time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(now - 1))}"
    valid_cookie = f"userid=42; Expires={time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(now + 10))}"
    cookie_header = f"{expired_cookie}, {valid_cookie}"

    result = get_expired_cookies(cookie_header, now=now)

    # Only the expired cookie should be returned
    assert len(result) == 1
    assert result[0]["name"] == "sessionid"
    assert result[0]["path"] == "/"  # default path

def test_get_expired_cookies_with_max_age(tmp_path):
    # Cookie with max-age that should be translated to expires
    now = time.time()
    cookie_header = "token=xyz; Max-Age=5"
    # The cookie should be considered expired after 5 seconds
    result_before = get_expired_cookies(cookie_header, now=now)
    assert result_before == []  # not yet expired

    # After 6 seconds, it should be expired
    result_after = get_expired_cookies(cookie_header, now=now + 6)
    assert len(result_after) == 1
    assert result_after[0]["name"] == "token"

def test_get_expired_cookies_handles_missing_expires_and_max_age(tmp_path):
    # Cookie without Expires or Max-Age should never be considered expired
    now = time.time()
    cookie_header = "foo=bar; Path=/; HttpOnly"
    result = get_expired_cookies(cookie_header, now=now)
    assert result == []  # no expiration info, so not expired
