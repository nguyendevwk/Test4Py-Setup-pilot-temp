import pytest
from string_utils.validation import is_url

def test_is_url_valid_and_scheme_filtering():
    # Normal valid URLs
    assert is_url('http://www.example.com') is True
    assert is_url('https://example.com/path?query=1') is True
    # Scheme filtering: only allow https
    assert is_url('https://example.com', allowed_schemes=['https']) is True
    # Scheme filtering: disallow http
    assert is_url('http://example.com', allowed_schemes=['https']) is False
    # Allowed schemes list with multiple entries
    assert is_url('ftp://example.com', allowed_schemes=['ftp', 'http']) is True

def test_is_url_boundary_cases():
    # Empty string or whitespace should be invalid
    assert is_url('') is False
    assert is_url('   ') is False
    # Non-string input should be invalid
    assert is_url(None) is False
    assert is_url(123) is False
    # String that looks like a URL but missing scheme
    assert is_url('www.example.com') is False
    # String with invalid characters
    assert is_url('http://exa mple.com') is False

def test_is_url_error_and_edge_conditions():
    # URL with uncommon but valid scheme
    assert is_url('mailto:user@example.com') is True
    # URL with port number
    assert is_url('http://localhost:8080') is True
    # URL with fragment
    assert is_url('https://example.com#section') is True
    # URL with query parameters containing special characters
    assert is_url('https://example.com/search?q=python+regex') is True
    # URL with path containing percent-encoded characters
    assert is_url('https://example.com/path%20with%20spaces') is True
