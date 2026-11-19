import pytest
from typesystem.formats import URLFormat

# Test 1: Valid URL should be returned unchanged
def test_urlformat_valid_url():
    fmt = URLFormat()
    url = "https://example.com/path?query=123"
    result = fmt.validate(url)
    assert result == url
    # serialize should return the same string
    assert fmt.serialize(result) == url

# Test 2: URL missing scheme should raise ValidationError
def test_urlformat_missing_scheme():
    fmt = URLFormat()
    bad_url = "example.com/path"
    with pytest.raises(Exception) as excinfo:
        fmt.validate(bad_url)
    # The exception should be a ValidationError with the correct message
    assert hasattr(excinfo.value, "message")
    assert "Must be a real URL." in str(excinfo.value)

# Test 3: serialize(None) should return None
def test_urlformat_serialize_none():
    fmt = URLFormat()
    assert fmt.serialize(None) is None
