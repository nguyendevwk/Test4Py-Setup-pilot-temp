import pytest
from typesystem.formats import URLFormat
from typesystem.base import ValidationError

def test_valid_url_returns_string():
    fmt = URLFormat()
    url = "https://example.com/path?query=1"
    result = fmt.validate(url)
    assert result == url
    # serialize should return the same string
    assert fmt.serialize(result) == url

def test_invalid_url_missing_scheme_raises():
    fmt = URLFormat()
    invalid_url = "example.com/path"
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate(invalid_url)
    assert "Must be a real URL." in str(excinfo.value)

def test_serialize_none_returns_none():
    fmt = URLFormat()
    assert fmt.serialize(None) is None
