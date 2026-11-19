import pytest
from string_utils.validation import is_ip_v6

def test_valid_ipv6_address():
    """A correctly formatted IPv6 address should return True."""
    addr = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    assert is_ip_v6(addr) is True

def test_invalid_ipv6_address():
    """An address with an illegal character should return False."""
    addr = "2001:0db8:85a3:0000:0000:8a2e:0370:733g"  # 'g' is not a hex digit
    assert is_ip_v6(addr) is False

def test_non_string_input_raises():
    """Passing a non-string type should raise a TypeError."""
    with pytest.raises(TypeError):
        is_ip_v6(12345)
