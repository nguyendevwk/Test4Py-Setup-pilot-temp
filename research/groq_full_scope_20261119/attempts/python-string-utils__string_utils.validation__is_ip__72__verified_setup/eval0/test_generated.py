import pytest
from string_utils.validation import is_ip

def test_is_ip_valid_ipv4_and_ipv6():
    """Verify that valid IPv4 and IPv6 addresses return True."""
    assert is_ip("192.168.0.1") is True
    assert is_ip("255.255.255.255") is True
    assert is_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334") is True
    assert is_ip("::1") is True

def test_is_ip_invalid_boundary_cases():
    """Verify that boundary/invalid IP strings return False."""
    # Octet out of range
    assert is_ip("256.100.50.25") is False
    # Too few octets
    assert is_ip("1.2.3") is False
    # Too many octets
    assert is_ip("1.2.3.4.5") is False
    # Invalid IPv6 format
    assert is_ip("2001:db8:::1") is False
    # Empty string
    assert is_ip("") is False

def test_is_ip_non_string_input():
    """Verify that non-string inputs are handled gracefully and return False."""
    assert is_ip(12345) is False
    assert is_ip(None) is False
    assert is_ip(["192.168.0.1"]) is False
