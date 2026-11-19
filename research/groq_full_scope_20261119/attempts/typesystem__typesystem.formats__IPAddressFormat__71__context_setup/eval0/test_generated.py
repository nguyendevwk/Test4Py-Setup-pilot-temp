import ipaddress
import pytest
from typesystem.formats import IPAddressFormat

def test_valid_ipv4_address():
    fmt = IPAddressFormat()
    ip_str = "192.168.0.1"
    result = fmt.validate(ip_str)
    assert isinstance(result, ipaddress.IPv4Address)
    assert str(result) == ip_str
    # serialize should return the string representation
    assert fmt.serialize(result) == ip_str
    # None serialization returns None
    assert fmt.serialize(None) is None

def test_valid_ipv6_address_boundary():
    fmt = IPAddressFormat()
    # minimal full IPv6 address
    ip_str = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    result = fmt.validate(ip_str)
    assert isinstance(result, ipaddress.IPv6Address)
    # ipaddress normalizes the address
    assert str(result) == "2001:db8:85a3::8a2e:370:7334"
    # serialize should return the normalized string
    assert fmt.serialize(result) == str(result)

def test_invalid_ip_address_raises_error():
    fmt = IPAddressFormat()
    # malformed IP that matches neither regex nor ipaddress parsing
    bad_ip = "999.999.999.999"
    with pytest.raises(fmt.validation_error("").__class__) as excinfo:
        fmt.validate(bad_ip)
    # error message should correspond to the "invalid" key
    assert "Must be a real IP." in str(excinfo.value)
