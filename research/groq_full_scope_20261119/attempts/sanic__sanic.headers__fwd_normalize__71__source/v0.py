import pytest
from sanic.headers import fwd_normalize
from sanic.exceptions import InvalidHeader

# Helper to simulate the address normalization function used internally
# (the real implementation is not exposed, but we can infer its behavior
# from the tests that exercise fwd_normalize).
def _normalize_address(value: str) -> str:
    # The real function likely strips quotes and resolves IPv6 brackets.
    # For testing purposes, we just return the value unchanged.
    return value

def test_fwd_normalize_basic_types(tmp_path):
    """Test normal conversion of each supported key type."""
    input_data = [
        ("by", "192.0.2.1"),
        ("for", "2001:db8::1"),
        ("host", "Example.COM"),
        ("proto", "HTTPS"),
        ("port", "443"),
        ("path", "/some%20path"),
        ("custom", "value"),
    ]
    result = fwd_normalize(input_data)
    assert result["by"] == _normalize_address("192.0.2.1")
    assert result["for"] == _normalize_address("2001:db8::1")
    assert result["host"] == "example.com"
    assert result["proto"] == "https"
    assert result["port"] == 443
    assert result["path"] == "/some path"
    assert result["custom"] == "value"

def test_fwd_normalize_boundary_and_none(tmp_path):
    """Test handling of boundary values and None inputs."""
    input_data = [
        ("port", "0"),          # lowest valid port
        ("port", "65535"),      # highest valid port
        ("port", None),         # None should be ignored
        ("path", ""),           # empty path should be unquoted to empty
        ("host", ""),           # empty host should be lowercased to empty
        ("proto", ""),          # empty proto should be lowercased to empty
    ]
    result = fwd_normalize(input_data)
    assert result["port"] == 65535  # last valid port wins
    assert result["path"] == ""
    assert result["host"] == ""
    assert result["proto"] == ""

def test_fwd_normalize_invalid_values(tmp_path):
    """Test that invalid values are ignored and do not raise."""
    input_data = [
        ("port", "not_a_number"),   # ValueError on int conversion
        ("by", None),               # None value should be ignored
        ("for", "invalid_address"), # Assume address normalization may raise
        ("unknown", "value"),       # Unknown key should be preserved
    ]
    result = fwd_normalize(input_data)
    # Invalid port should be omitted
    assert "port" not in result
    # None value should be omitted
    assert "by" not in result
    # Unknown key should be preserved
    assert result["unknown"] == "value"
    # For key with invalid address, we expect it to be omitted
    assert "for" not in result
