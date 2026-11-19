import pytest
import ipaddress
from typesystem.formats import IPAddressFormat
from typesystem.base import ValidationError

def test_valid_ipv4_address():
    fmt = IPAddressFormat()
    result = fmt.validate("192.168.1.1")
    assert isinstance(result, ipaddress.IPv4Address)
    assert str(result) == "192.168.1.1"
    # serialization should return the string representation
    assert fmt.serialize(result) == "192.168.1.1"

def test_invalid_format_raises_validation_error():
    fmt = IPAddressFormat()
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("not.an.ip")
    # The error message should correspond to the 'format' key
    assert "Must be a valid IP format." in str(excinfo.value)

def test_invalid_ip_value_raises_validation_error():
    fmt = IPAddressFormat()
    # This string matches the IPv4 regex but is not a real IP address
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate("999.999.999.999")
    # The error message should correspond to the 'invalid' key
    assert "Must be a real IP." in str(excinfo.value)
