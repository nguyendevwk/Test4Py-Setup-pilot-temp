import pytest
from string_utils.validation import is_url

def test_is_url_valid_and_scheme_filtering():
    # Valid URLs
    assert is_url("http://example.com") is True
    assert is_url("https://example.com/path?query=1") is True
    # Scheme filtering: only allow https
    assert is_url("https://example.com", allowed_schemes=["https"]) is True
    # Scheme filtering: disallow http
    assert is_url("http://example.com", allowed_schemes=["https"]) is False
    # Multiple allowed schemes
    assert is_url("ftp://example.com", allowed_schemes=["ftp", "http"]) is True

def test_is_url_boundary_cases():
    # Empty string should be invalid
    assert is_url("") is False
    # String with only whitespace should be invalid
    assert is_url("   ") is False
    # URL with unusual but valid characters
    assert is_url("http://sub.domain.com:8080/path?name=value#fragment") is True

def test_is_url_invalid_inputs():
    # Non-string input should be treated as invalid
    assert is_url(12345) is False
    assert is_url(None) is False
    # String that looks like a URL but is malformed
    assert is_url("http://") is False
    assert is_url("://example.com") is False
