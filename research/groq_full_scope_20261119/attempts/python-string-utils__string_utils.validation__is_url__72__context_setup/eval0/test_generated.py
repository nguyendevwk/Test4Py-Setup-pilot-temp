import pytest
from string_utils.validation import is_url

def test_is_url_valid_and_scheme_allowed():
    # Normal case: valid URL with allowed scheme
    url = "https://example.com/path?query=1"
    assert is_url(url, allowed_schemes=["https", "http"]) is True
    # Scheme not in allowed list should return False
    assert is_url(url, allowed_schemes=["http"]) is False

def test_is_url_invalid_and_boundary_cases():
    # Boundary: empty string and whitespace only
    assert is_url("") is False
    assert is_url("   ") is False
    # Invalid URL format
    assert is_url("not_a_url") is False
    # URL with unsupported scheme but allowed_schemes is None
    assert is_url("ftp://example.com") is True

def test_is_url_non_string_input_and_edge_schemes():
    # Non-string input should be treated as invalid
    assert is_url(12345) is False
    # URL starting with a dot is invalid
    assert is_url(".example.com") is False
    # URL with uppercase scheme should match allowed list case-sensitively
    assert is_url("HTTP://example.com") is False
    assert is_url("HTTP://example.com", allowed_schemes=["HTTP"]) is True
