import pytest
from sanic.headers import fwd_normalize

def test_fwd_normalize_basic_types():
    """Test normal conversion of host, proto, port, and path."""
    input_data = [
        ("host", "Example.COM"),
        ("proto", "HTTPS"),
        ("port", "443"),
        ("path", "/some%20path/"),
        ("custom", "value"),
    ]
    result = fwd_normalize(input_data)
    assert result == {
        "host": "example.com",
        "proto": "https",
        "port": 443,
        "path": "/some path/",
        "custom": "value",
    }

def test_fwd_normalize_none_and_invalid_int():
    """Test that None values are ignored and invalid integers are skipped."""
    input_data = [
        ("host", None),          # should be ignored
        ("port", "not_a_number"),  # ValueError, should be ignored
        ("by", "192.168.1.1"),   # fwd_normalize_address will be called; result depends on implementation
    ]
    result = fwd_normalize(input_data)
    # 'by' key should be present if fwd_normalize_address returns a value; otherwise it may be omitted.
    # We only assert that host and port are absent.
    assert "host" not in result
    assert "port" not in result
    # The 'by' key should be present and be a string (implementation dependent)
    assert "by" in result
    assert isinstance(result["by"], str)

def test_fwd_normalize_unquote_and_lowercase():
    """Test that percent-encoded paths are unquoted and host/proto are lowercased."""
    input_data = [
        ("path", "%2Ffoo%2Fbar%20baz"),
        ("host", "LOCALHOST"),
        ("proto", "HTTP"),
    ]
    result = fwd_normalize(input_data)
    assert result["path"] == "/foo/bar baz"
    assert result["host"] == "localhost"
    assert result["proto"] == "http"
