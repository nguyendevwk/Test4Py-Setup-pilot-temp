import pytest
from sanic.headers import fwd_normalize, fwd_normalize_address, InvalidHeader

def test_fwd_normalize_basic_types():
    # Basic header values should be converted appropriately
    input_headers = [
        ("host", "Example.COM"),
        ("proto", "HTTPS"),
        ("port", "443"),
        ("path", "/some%20path"),
        ("by", "192.168.1.1"),
        ("for", "2001:db8::1"),
        ("custom", "value"),
    ]
    result = fwd_normalize(input_headers)
    assert result == {
        "host": "example.com",
        "proto": "https",
        "port": 443,
        "path": "/some path",
        "by": "192.168.1.1",
        "for": "[2001:db8::1]",
        "custom": "value",
    }

def test_fwd_normalize_address_edge_cases():
    # Addresses that should raise ValueError or be left unchanged
    input_headers = [
        ("by", "unknown"),          # should be omitted
        ("for", "_obfuscated"),     # should remain unchanged
        ("by", "2001:db8::2"),      # IPv6 should be bracketed
        ("by", "10.0.0.1"),         # IPv4 should stay as is
    ]
    result = fwd_normalize(input_headers)
    assert "by" not in result or result["by"] == "10.0.0.1"  # unknown omitted
    assert result.get("for") == "_obfuscated"
    assert result.get("by") == "[2001:db8::2]" or result.get("by") == "10.0.0.1"

def test_fwd_normalize_invalid_values():
    # Invalid numeric or unparsable values should be ignored
    input_headers = [
        ("port", "not_a_number"),
        ("path", None),          # None values are skipped
        ("proto", "HTTP/1.1"),   # lowercased but contains slash
        ("by", "unknown"),       # omitted
    ]
    result = fwd_normalize(input_headers)
    assert "port" not in result
    assert result["proto"] == "http/1.1"
    assert "by" not in result
