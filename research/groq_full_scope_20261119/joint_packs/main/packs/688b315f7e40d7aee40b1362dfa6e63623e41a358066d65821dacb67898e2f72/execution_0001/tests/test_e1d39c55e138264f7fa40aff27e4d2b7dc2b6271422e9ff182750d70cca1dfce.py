import pytest
from httpie.utils import split_cookies

def test_split_cookies_normal():
    # Two cookies, simple values
    cookie_header = "sessionid=abc123; Path=/, csrftoken=xyz789; Path=/"
    result = split_cookies(cookie_header)
    assert result == ["sessionid=abc123; Path=/", "csrftoken=xyz789; Path=/"]

def test_split_cookies_empty_and_none():
    # Empty string should return empty list
    assert split_cookies("") == []
    # None should also return empty list
    assert split_cookies(None) == []

def test_split_cookies_with_comma_in_value():
    # Cookie value contains a comma; should not split on it
    cookie_header = "data=part1,part2; Path=/, token=abc; Path=/"
    result = split_cookies(cookie_header)
    assert result == ["data=part1,part2; Path=/", "token=abc; Path=/"]
