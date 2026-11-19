import pytest
from typesystem.formats import URLFormat
from typesystem.base import ValidationError

def test_urlformat_valid_url():
    fmt = URLFormat()
    url = "https://example.com/path?query=1"
    result = fmt.validate(url)
    assert result == url
    # serialize should return the same string
    assert fmt.serialize(result) == url

def test_urlformat_missing_scheme():
    fmt = URLFormat()
    url = "example.com/path"
    with pytest.raises(ValidationError) as excinfo:
        fmt.validate(url)
    assert "invalid" in str(excinfo.value)

def test_urlformat_none_serialization():
    fmt = URLFormat()
    # serialize should return None when given None
    assert fmt.serialize(None) is None
