import ipaddress
import pytest
from typesystem.formats import IPAddressFormat

def test_valid_ipv4_address():
    fmt = IPAddressFormat()
    ip_str = "192.168.1.1"
    result = fmt.validate(ip_str)
    assert isinstance(result, ipaddress.IPv4Address)
    assert str(result) == ip_str
    serialized = fmt.serialize(result)
    assert serialized == ip_str

def test_invalid_format_raises_validation_error():
    fmt = IPAddressFormat()
    bad_ip = "999.999.999.999"
    with pytest.raises(fmt.validation_error("").__class__) as excinfo:
        fmt.validate(bad_ip)
    assert "format" in excinfo.value.code
    assert "Must be a valid IP format." in excinfo.value.text

def test_invalid_ip_value_raises_validation_error():
    fmt = IPAddressFormat()
    bad_ip = "256.256.256.256"
    with pytest.raises(fmt.validation_error("").__class__) as excinfo:
        fmt.validate(bad_ip)
    assert "invalid" in excinfo.value.code
    assert "Must be a real IP." in excinfo.value.text
