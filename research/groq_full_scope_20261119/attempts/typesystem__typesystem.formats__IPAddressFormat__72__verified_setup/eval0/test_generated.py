import ipaddress
import pytest
from typesystem.formats import IPAddressFormat

# Test that a valid IPv4 address is accepted and returned as an ipaddress.IPv4Address instance
def test_valid_ipv4_address():
    fmt = IPAddressFormat()
    result = fmt.validate("192.168.1.1")
    assert isinstance(result, ipaddress.IPv4Address)
    assert str(result) == "192.168.1.1"

# Test that a valid IPv6 address is accepted and returned as an ipaddress.IPv6Address instance
def test_valid_ipv6_address():
    fmt = IPAddressFormat()
    result = fmt.validate("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
    assert isinstance(result, ipaddress.IPv6Address)
    assert str(result) == "2001:db8:85a3::8a2e:370:7334"

# Test that an invalid IP string raises a ValidationError with the correct message
def test_invalid_ip_address():
    fmt = IPAddressFormat()
    with pytest.raises(fmt.ValidationError) as excinfo:
        fmt.validate("999.999.999.999")
    assert "Must be a real IP." in str(excinfo.value)
