import pytest
from string_utils.validation import is_ip_v4

def test_valid_ipv4_addresses():
    """Normal case: valid IPv4 addresses should return True."""
    assert is_ip_v4("192.168.0.1") is True
    assert is_ip_v4("0.0.0.0") is True
    assert is_ip_v4("255.255.255.255") is True

def test_boundary_and_invalid_values():
    """Boundary values and out‑of‑range numbers should return False."""
    # Out of range octet
    assert is_ip_v4("256.100.50.25") is False
    # Negative number
    assert is_ip_v4("-1.10.20.30") is False
    # Too many octets
    assert is_ip_v4("1.2.3.4.5") is False
    # Too few octets
    assert is_ip_v4("1.2.3") is False
    # Non‑numeric characters
    assert is_ip_v4("a.b.c.d") is False

def test_non_string_inputs():
    """Non‑string inputs should be treated as invalid and return False."""
    assert is_ip_v4(12345) is False
    assert is_ip_v4(None) is False
    assert is_ip_v4(["192", "168", "0", "1"]) is False
