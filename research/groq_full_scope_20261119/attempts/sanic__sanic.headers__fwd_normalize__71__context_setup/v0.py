import pytest
from sanic.headers import fwd_normalize, fwd_normalize_address

def test_fwd_normalize_basic_types():
    # Basic key/value pairs with different expected conversions
    input_iter = [
        ("by", "192.0.2.1"),
        ("for", "2001:db8::1"),
        ("host", "Example.COM"),
        ("proto", "HTTPS"),
        ("port", "443"),
        ("path", "/foo%20bar"),
        ("custom", "value"),
    ]
    result = fwd_normalize(input_iter)
    assert result == {
        "by": "192.0.2.1",
        "for": "[2001:db8::1]",          # IPv6 bracketed and lowercased
        "host": "example.com",
        "proto": "https",
        "port": 443,
        "path": "/foo bar",
        "custom": "value",
    }

def test_fwd_normalize_address_edge_cases():
    # Address normalization edge cases: unknown, obfuscated, IPv6
    assert fwd_normalize_address("unknown") is None  # ValueError swallowed in fwd_normalize
    with pytest.raises(ValueError):
        fwd_normalize_address("unknown")  # direct call should raise

    # Obfuscated string starting with underscore should remain unchanged
    assert fwd_normalize_address("_obf") == "_obf"

    # IPv6 address should be bracketed and lowercased
    ipv6 = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    assert fwd_normalize_address(ipv6) == f"[{ipv6.lower()}]"

def test_fwd_normalize_error_handling():
    # Invalid integer for port and malformed IPv6 should be ignored
    input_iter = [
        ("port", "not_an_int"),
        ("by", "invalid_ipv6"),  # not matching IPv6 regex, should be lowercased
        ("for", "unknown"),      # should be omitted
    ]
    result = fwd_normalize(input_iter)
    assert result == {
        "by": "invalid_ipv6",
    }
    # Ensure that the 'for' key is omitted due to ValueError
    assert "for" not in result
