import re
import pytest
from httpie.utils import split_cookies, RE_COOKIE_SPLIT

def test_split_cookies_basic():
    # A simple case with two cookies separated by a comma and space
    raw = "sessionid=abc123; Path=/, csrftoken=xyz456; Path=/"
    result = split_cookies(raw)
    assert result == ["sessionid=abc123; Path=/", "csrftoken=xyz456; Path=/"]
    # Ensure the regex used by the function matches the same pattern
    assert RE_COOKIE_SPLIT.pattern == r', (?=[^ ;]+=)'

def test_split_cookies_no_split_on_value_comma():
    # Cookie value contains a comma; it should not be split
    raw = "a=1,2,3; Path=/, b=4; Path=/"
    result = split_cookies(raw)
    assert result == ["a=1,2,3; Path=/", "b=4; Path=/"]

def test_split_cookies_empty_and_none():
    # Empty string and None should return an empty list
    assert split_cookies("") == []
    assert split_cookies(None) == []
