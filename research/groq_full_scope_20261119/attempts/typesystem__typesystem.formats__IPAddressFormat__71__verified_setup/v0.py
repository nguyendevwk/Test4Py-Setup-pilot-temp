import ipaddress
import pytest
from typesystem.formats import IPAddressFormat

def test_valid_ipv4_address():
    fmt = IPAddressFormat()
    # Valid IPv4 string
    ip_str = "192.168.1.1"
    result = fmt.validate(ip_str)
    assert isinstance(result, ipaddress.IPv4Address)
    assert str(result) == ip_str
    # Serialization returns the same string
    serialized = fmt.serialize(result)
    assert serialized == ip_str

def test_valid_ipv6_address_boundary():
    fmt = IPAddressFormat()
    # Valid IPv6 string (compressed form)
    ip_str = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    result = fmt.validate(ip_str)
    assert isinstance(result, ipaddress.IPv6Address)
    # ipaddress normalizes the representation
    assert str(result) == "2001:db8:85a3::8a2e:370:7334"
    # Serialization should match the normalized form
    assert fmt.serialize(result) == str(result)

def test_invalid_ip_address_raises():
    fmt = IPAddressFormat()
    # String that matches regex but is not a real IP
    invalid_str = "999.999.999.999"
    with pytest.raises(fmt.ValidationError) as excinfo:
        fmt.validate(invalid_str)
    # The error message should correspond to the "invalid" key
    assert "Must be a real IP." in str(excinfo.value)
