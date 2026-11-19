import pytest
from typesystem.formats import URLFormat
from typesystem.base import ValidationError

def test_validate_successful_url():
    fmt = URLFormat()
    url = "https://example.com/path?query=1"
    result = fmt.validate(url)
    assert result == url
    # Ensure that the parsed components are present
    parsed = fmt.validate(url)
    assert parsed == url

def test_validate_invalid_url_missing_scheme():
    fmt = URLFormat()
    invalid_url = "www.example.com"
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate(invalid_url)
    assert excinfo.value.code == "invalid"
    assert "Must be a real URL." in str(excinfo.value)

def test_serialize_none_and_valid():
    fmt = URLFormat()
    # Serializing None should return None
    assert fmt.serialize(None) is None
    # Serializing a valid URL string should return the same string
    url = "http://localhost"
    assert fmt.serialize(url) == url
