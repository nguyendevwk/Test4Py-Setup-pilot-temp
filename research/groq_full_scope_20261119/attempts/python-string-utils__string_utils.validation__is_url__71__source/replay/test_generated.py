import pytest
from string_utils.validation import is_url

def test_is_url_valid_and_invalid_cases():
    # Valid URLs
    assert is_url("http://www.example.com") is True
    assert is_url("https://example.com/path?query=1") is True
    # Invalid URLs
    assert is_url("not a url") is False
    assert is_url("http://") is False
    assert is_url(".example.com") is False
    # Empty string should be invalid
    assert is_url("") is False

def test_is_url_allowed_schemes_filtering():
    # URL with http scheme
    assert is_url("http://example.com", allowed_schemes=["https"]) is False
    # URL with https scheme
    assert is_url("https://example.com", allowed_schemes=["https"]) is True
    # Multiple allowed schemes
    assert is_url("ftp://example.com", allowed_schemes=["http", "https", "ftp"]) is True
    # No allowed schemes provided defaults to any scheme
    assert is_url("ftp://example.com") is True

def test_is_url_non_string_input():
    # Non-string inputs should be treated as invalid
    assert is_url(12345) is False
    assert is_url(None) is False
    assert is_url(["http://example.com"]) is False
