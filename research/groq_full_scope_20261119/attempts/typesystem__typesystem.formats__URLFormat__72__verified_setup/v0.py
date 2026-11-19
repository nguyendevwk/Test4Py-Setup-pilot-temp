import pytest
from typesystem.formats import URLFormat

# Test 1: Valid URL passes validation and returns the same string
def test_urlformat_valid_url():
    url_format = URLFormat()
    input_url = "https://example.com/path?query=1"
    result = url_format.validate(input_url)
    assert result == input_url
    # serialize should return the same string
    assert url_format.serialize(result) == input_url

# Test 2: URL missing scheme or netloc triggers ValidationError
def test_urlformat_invalid_url_missing_parts():
    url_format = URLFormat()
    # Missing scheme
    with pytest.raises(Exception) as excinfo:
        url_format.validate("www.example.com")
    assert "Must be a real URL." in str(excinfo.value)

    # Missing netloc
    with pytest.raises(Exception) as excinfo:
        url_format.validate("http:///path")
    assert "Must be a real URL." in str(excinfo.value)

# Test 3: serialize handles None correctly
def test_urlformat_serialize_none():
    url_format = URLFormat()
    assert url_format.serialize(None) is None
