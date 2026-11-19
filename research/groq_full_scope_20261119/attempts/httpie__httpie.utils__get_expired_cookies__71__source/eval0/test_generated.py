import time
import pytest
from httpie.utils import get_expired_cookies


def test_get_expired_cookies_with_expired_and_nonexpired(tmp_path):
    # Create a cookie string with two cookies: one expired, one not.
    now = time.time()
    expired_time = now - 10  # 10 seconds ago
    future_time = now + 1000  # 1000 seconds in the future

    # Cookie format: name=value; Expires=...
    cookie_str = (
        f"sessionid=abc123; Expires={time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(expired_time))}; "
        f"path=/; "
        f"userid=42; Expires={time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(future_time))}; "
        f"path=/profile"
    )

    expired = get_expired_cookies(cookie_str, now=now)

    # Only the expired cookie should be returned
    assert len(expired) == 1
    assert expired[0]['name'] == 'sessionid'
    assert expired[0]['path'] == '/'


def test_get_expired_cookies_boundary_expiration(tmp_path):
    # Cookie expires exactly at the current time should be considered expired.
    now = time.time()
    expire_at_now = now

    cookie_str = (
        f"token=xyz; Expires={time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime(expire_at_now))}; "
        f"path=/"
    )

    expired = get_expired_cookies(cookie_str, now=now)

    assert len(expired) == 1
    assert expired[0]['name'] == 'token'
    assert expired[0]['path'] == '/'


def test_get_expired_cookies_no_expires_and_empty_input(tmp_path):
    # Cookie without Expires attribute should never be considered expired.
    cookie_str = "user=alice; path=/dashboard"
    expired = get_expired_cookies(cookie_str, now=time.time())
    assert expired == []

    # Empty input should return an empty list without error.
    assert get_expired_cookies("", now=time.time()) == []
