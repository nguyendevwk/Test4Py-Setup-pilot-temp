import pytest
from string_utils.validation import is_ip_v4

def test_valid_ip_v4():
    """A correctly formatted IPv4 address should return True."""
    assert is_ip_v4('192.168.0.1') is True
    assert is_ip_v4('0.0.0.0') is True
    assert is_ip_v4('255.255.255.255') is True

def test_invalid_ip_v4_boundary_and_format():
    """Addresses with out‑of‑range octets or wrong format should return False."""
    # Octet out of range
    assert is_ip_v4('256.100.50.25') is False
    assert is_ip_v4('10.0.0.256') is False
    # Wrong number of octets
    assert is_ip_v4('1.2.3') is False
    assert is_ip_v4('1.2.3.4.5') is False
    # Non‑numeric characters
    assert is_ip_v4('abc.def.ghi.jkl') is False
    assert is_ip_v4('123.456.78.90') is False  # 456 out of range

def test_non_string_inputs():
    """Non‑string inputs should be treated as invalid and return False."""
    assert is_ip_v4(None) is False
    assert is_ip_v4(12345) is False
    assert is_ip_v4(['192', '168', '0', '1']) is False
    assert is_ip_v4({'ip': '192.168.0.1'}) is False
