import ipaddress
import pytest
from typesystem.formats import IPAddressFormat
from typesystem.base import ValidationError

def test_valid_ipv4_address():
    fmt = IPAddressFormat()
    result = fmt.validate("192.168.1.1")
    assert isinstance(result, ipaddress.IPv4Address)
    assert str(result) == "192.168.1.1"
    serialized = fmt.serialize(result)
    assert serialized == "192.168.1.1"

def test_invalid_format_raises_validation_error():
    fmt = IPAddressFormat()
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("not.an.ip")
    assert "format" in str(excinfo.value)

def test_invalid_ip_value_raises_validation_error():
    fmt = IPAddressFormat()
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("256.256.256.256")
    assert "invalid" in str(excinfo.value)
