import re
import pytest
from httpie.utils import split_cookies, RE_COOKIE_SPLIT


def test_split_cookies_basic():
    """Verify that a simple comma‑separated string is split correctly."""
    raw = "sessionid=abc123, csrftoken=xyz456"
    result = split_cookies(raw)
    assert result == ["sessionid=abc123", "csrftoken=xyz456"]
    # Ensure the regex does not split on commas inside values
    assert all(re.search(r'^[^=]+=[^,]+$', part) for part in result)


def test_split_cookies_with_comma_in_value():
    """Ensure commas inside cookie values are preserved."""
    raw = "token=abc,def,ghi, user=joe"
    result = split_cookies(raw)
    # The first cookie value contains commas; only the separator comma is split
    assert result == ["token=abc,def,ghi", "user=joe"]
    # The regex should not split on commas that are not followed by a key=value pattern
    assert all(re.search(r'^[^=]+=[^,]+$', part) for part in result)


def test_split_cookies_empty_and_none():
    """split_cookies should return an empty list for falsy inputs."""
    assert split_cookies("") == []
    assert split_cookies(None) == []
    assert split_cookies([]) == []
