import pytest
from string_utils.validation import is_ip_v4

def test_valid_ip_addresses():
    """Normal valid IPs should return True."""
    assert is_ip_v4('192.168.0.1') is True
    assert is_ip_v4('10.0.0.255') is True
    assert is_ip_v4('0.0.0.0') is True
    assert is_ip_v4('255.255.255.255') is True

def test_boundary_and_invalid_values():
    """Boundary values and out‑of‑range numbers should be handled correctly."""
    # Boundary values are valid
    assert is_ip_v4('0.0.0.0') is True
    assert is_ip_v4('255.255.255.255') is True
    # Out of range values should be invalid
    assert is_ip_v4('256.100.50.25') is False
    assert is_ip_v4('192.168.1.256') is False
    # Non‑numeric parts should be invalid
    assert is_ip_v4('192.168.one.1') is False
    assert is_ip_v4('...') is False

def test_non_string_inputs_and_empty():
    """Non‑string inputs and empty strings should return False without raising."""
    assert is_ip_v4(12345) is False
    assert is_ip_v4(None) is False
    assert is_ip_v4('') is False
    assert is_ip_v4('   ') is False
