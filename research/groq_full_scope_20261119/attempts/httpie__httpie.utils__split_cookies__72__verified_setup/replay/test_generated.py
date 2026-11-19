import pytest
from httpie.utils import split_cookies

def test_split_cookies_single():
    # A single cookie string should return a list with that string
    cookie_str = "sessionid=abc123; Path=/; HttpOnly"
    result = split_cookies(cookie_str)
    assert isinstance(result, list)
    assert result == [cookie_str]

def test_split_cookies_multiple_with_comma_in_value():
    # Multiple cookies separated by commas, but one value contains a comma
    cookie_str = (
        "id=1; Path=/, "
        "token=abc,def; Path=/, "
        "lang=en; Path=/"
    )
    result = split_cookies(cookie_str)
    # Should split into three cookies, preserving the comma inside the token value
    assert result == [
        "id=1; Path=/",
        "token=abc,def; Path=/",
        "lang=en; Path=/"
    ]

def test_split_cookies_empty_and_none():
    # Empty string or None should return an empty list
    assert split_cookies("") == []
    assert split_cookies(None) == []
