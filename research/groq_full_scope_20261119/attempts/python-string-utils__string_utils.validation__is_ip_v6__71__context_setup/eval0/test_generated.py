import pytest
from string_utils.validation import is_ip_v6

def test_valid_ipv6_address():
    """A correctly formatted IPv6 address should return True."""
    addr = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    assert is_ip_v6(addr) is True

def test_invalid_ipv6_address_with_nonhex_character():
    """An IPv6 address containing a non-hex character should return False."""
    addr = "2001:0db8:85a3:0000:0000:8a2e:0370:733g"  # 'g' is not a hex digit
    assert is_ip_v6(addr) is False

def test_non_string_input_returns_false():
    """Non-string inputs should be treated as invalid and return False."""
    assert is_ip_v6(12345) is False
    assert is_ip_v6(None) is False
    assert is_ip_v6(b"2001:db8::1") is False
