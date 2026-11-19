import re
import pytest
from httpie.utils import split_cookies

# The regex used internally by split_cookies is not part of the public API,
# but we can access it via the module's globals for testing purposes.
RE_COOKIE_SPLIT = re.compile(r',\s*(?=[^=]+=)')

def test_split_cookies_normal():
    """
    Verify that split_cookies correctly splits a header string containing
    multiple cookies, even when a cookie value contains a comma.
    """
    header = (
        "sessionid=abc123, "
        "theme=light, "
        "prefs=lang=en,us, "
        "token=xyz,789"
    )
    result = split_cookies(header)
    # Expected split: each cookie name=value pair
    expected = [
        "sessionid=abc123",
        "theme=light",
        "prefs=lang=en,us",
        "token=xyz,789"
    ]
    assert result == expected, f"Expected {expected}, got {result}"
    # Ensure that the split regex did not split inside values
    assert all(',' not in cookie.split('=')[1] or cookie.split('=')[1] in ["lang=en,us", "xyz,789"] for cookie in result)

def test_split_cookies_empty_and_none():
    """
    split_cookies should return an empty list for falsy inputs.
    """
    assert split_cookies("") == [], "Empty string should return empty list"
    assert split_cookies(None) == [], "None should return empty list"
    assert split_cookies([]) == [], "Empty list should return empty list"

def test_split_cookies_single_cookie_no_comma():
    """
    When the header contains a single cookie without any commas,
    the function should return a list with that single cookie.
    """
    header = "user=alice"
    result = split_cookies(header)
    assert result == ["user=alice"], f"Expected ['user=alice'], got {result}"
    # Ensure no accidental splitting
    assert len(result) == 1
