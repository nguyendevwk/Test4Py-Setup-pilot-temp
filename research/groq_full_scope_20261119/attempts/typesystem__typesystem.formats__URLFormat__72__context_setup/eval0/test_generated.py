import pytest
from typesystem.formats import URLFormat
from typesystem.base import ValidationError

def test_validate_successful_url():
    fmt = URLFormat()
    url = "https://example.com/path?query=1"
    result = fmt.validate(url)
    assert result == url
    # Ensure that the returned value is a string
    assert isinstance(result, str)

def test_validate_invalid_url_missing_scheme():
    fmt = URLFormat()
    invalid_url = "example.com/path"
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate(invalid_url)
    # The error message should match the defined error text
    assert str(excinfo.value) == "Must be a real URL."
    # The error code should be 'invalid'
    assert excinfo.value.code == "invalid"

def test_serialize_none_and_string():
    fmt = URLFormat()
    # Serializing None should return None
    assert fmt.serialize(None) is None
    # Serializing a valid URL string should return the same string
    url = "https://example.com"
    assert fmt.serialize(url) == url
