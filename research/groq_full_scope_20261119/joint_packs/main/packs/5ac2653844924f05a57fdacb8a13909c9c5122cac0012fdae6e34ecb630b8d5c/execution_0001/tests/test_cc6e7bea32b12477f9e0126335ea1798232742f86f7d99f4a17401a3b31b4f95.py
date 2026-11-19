import pytest
from string_utils.validation import is_url

def test_is_url_valid_and_invalid_cases():
    # Valid URLs
    assert is_url("http://www.example.com") is True
    assert is_url("https://sub.domain.co.uk/path?query=1") is True
    # Invalid URLs
    assert is_url("not a url") is False
    assert is_url(".example.com") is False
    assert is_url("http://") is False

def test_is_url_allowed_schemes_filtering():
    # URL with http scheme
    assert is_url("http://example.com", allowed_schemes=["https"]) is False
    assert is_url("http://example.com", allowed_schemes=["http", "https"]) is True
    # URL with https scheme
    assert is_url("https://example.com", allowed_schemes=["https"]) is True
    assert is_url("https://example.com", allowed_schemes=["ftp"]) is False

def test_is_url_non_string_input_returns_false():
    # Non-string inputs should be treated as invalid URLs
    assert is_url(12345) is False
    assert is_url(None) is False
    assert is_url(["http://example.com"]) is False
