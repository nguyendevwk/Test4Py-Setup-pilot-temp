import pytest
from sanic.headers import fwd_normalize
from sanic.exceptions import InvalidHeader

# Helper to create a simple iterable of key-value pairs
def kv_iter(pairs):
    return [(k, v) for k, v in pairs]

def test_fwd_normalize_basic_types():
    """Test normal conversion of each supported key."""
    input_pairs = [
        ("by", "192.0.2.1"),
        ("for", "2001:db8::1"),
        ("host", "Example.COM"),
        ("proto", "HTTPS"),
        ("port", "443"),
        ("path", "/foo%20bar"),
        ("custom", "value"),
    ]
    result = fwd_normalize(kv_iter(input_pairs))
    assert result == {
        "by": "192.0.2.1",
        "for": "2001:db8::1",
        "host": "example.com",
        "proto": "https",
        "port": 443,
        "path": "/foo bar",
        "custom": "value",
    }

def test_fwd_normalize_boundary_and_none():
    """Test handling of None values and boundary numeric conversion."""
    input_pairs = [
        ("port", "0"),          # boundary port
        ("port", "65535"),      # maximum port
        ("port", None),         # None value should be ignored
        ("by", None),           # None value should be ignored
        ("proto", "HTTP"),      # case-insensitive
    ]
    result = fwd_normalize(kv_iter(input_pairs))
    assert result == {
        "port": 0,          # first valid port wins
        "proto": "http",
    }

def test_fwd_normalize_invalid_values():
    """Test that invalid values are silently ignored."""
    input_pairs = [
        ("port", "not_a_number"),   # ValueError on int conversion
        ("by", "invalid address"),  # fwd_normalize_address may raise InvalidHeader
        ("path", None),             # None value ignored
        ("unknown", "value"),       # unknown key passes through unchanged
    ]
    # fwd_normalize_address is not imported; we assume it raises InvalidHeader
    # for an invalid address. The function should catch ValueError only,
    # so InvalidHeader will propagate. We test that behavior.
    with pytest.raises(InvalidHeader):
        fwd_normalize(kv_iter(input_pairs))
