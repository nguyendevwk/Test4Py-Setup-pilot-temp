import time
import pytest
from httpie.utils import get_expired_cookies

def test_expired_cookies_with_expiration():
    # Cookie with explicit expires timestamp in the past
    past_ts = int(time.time()) - 10
    cookie_str = f"sessionid=abc123; Expires={past_ts}"
    expired = get_expired_cookies(cookie_str, now=time.time())
    assert len(expired) == 1
    assert expired[0]["name"] == "sessionid"
    assert expired[0]["path"] == "/"

def test_expired_cookies_boundary_equal_now():
    # Cookie expires exactly at the current time should be considered expired
    now_ts = int(time.time())
    cookie_str = f"token=xyz; Expires={now_ts}"
    expired = get_expired_cookies(cookie_str, now=now_ts)
    assert expired == [{"name": "token", "path": "/"}]

def test_no_expiration_and_empty_input():
    # Cookie without an Expires attribute should not be returned
    cookie_str = "user=alice; Path=/"
    expired = get_expired_cookies(cookie_str, now=time.time())
    assert expired == []

    # Empty cookie string should yield an empty list without error
    assert get_expired_cookies("", now=time.time()) == []
