import pytest
from string_utils.validation import is_ip

def test_is_ip_valid_ipv4_and_ipv6():
    # Valid IPv4 address
    assert is_ip("192.168.0.1") is True
    # Valid IPv6 address
    assert is_ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334") is True
    # Edge case: IPv4 with leading zeros
    assert is_ip("001.002.003.004") is True

def test_is_ip_invalid_and_boundary_cases():
    # Invalid IPv4 (too few octets)
    assert is_ip("1.2.3") is False
    # Invalid IPv4 (octet > 255)
    assert is_ip("256.100.50.25") is False
    # Invalid IPv6 (wrong format)
    assert is_ip("2001:db8:::1") is False
    # Empty string
    assert is_ip("") is False

def test_is_ip_non_string_inputs():
    # Non-string inputs should be handled gracefully
    assert is_ip(12345) is False
    assert is_ip(None) is False
    assert is_ip(["192.168.0.1"]) is False
