import pytest
from httpie.utils import split_cookies

def test_split_cookies_basic():
    # A typical Set-Cookie header with two cookies separated by a comma
    header = "sessionid=abc123; Path=/, csrftoken=xyz789; Path=/"
    result = split_cookies(header)
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].startswith("sessionid=")
    assert result[1].startswith("csrftoken=")

def test_split_cookies_no_cookies():
    # Empty string should return an empty list
    assert split_cookies("") == []
    # None should also return an empty list
    assert split_cookies(None) == []

def test_split_cookies_complex_values():
    # Cookie values may contain commas; ensure they are not split
    header = "id=1,2,3; Path=/, token=abc,def; Path=/"
    result = split_cookies(header)
    assert len(result) == 2
    # The first cookie value should preserve commas
    assert result[0] == "id=1,2,3; Path=/"
    # The second cookie value should also preserve commas
    assert result[1] == "token=abc,def; Path=/"
