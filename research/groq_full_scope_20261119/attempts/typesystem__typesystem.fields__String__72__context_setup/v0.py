import re
import pytest
from typesystem.fields import String

def test_string_valid_and_trim():
    # allow_blank=False, trim_whitespace=True
    field = String()
    # Leading/trailing whitespace should be stripped
    assert field.validate("  hello  ") == "hello"
    # Null character removed
    assert field.validate("he\0llo") == "hello"
    # Empty string is invalid when allow_blank=False
    with pytest.raises(Exception) as excinfo:
        field.validate("")
    assert "blank" in str(excinfo.value)

def test_string_max_length_boundary():
    # max_length=5, allow_blank=True
    field = String(max_length=5, allow_blank=True)
    # Exactly at limit
    assert field.validate("12345") == "12345"
    # Exceeds limit
    with pytest.raises(Exception) as excinfo:
        field.validate("123456")
    assert "max_length" in str(excinfo.value)

def test_string_pattern_mismatch():
    # pattern requires digits only
    field = String(pattern=r"^\d+$")
    # Valid numeric string
    assert field.validate("123") == "123"
    # Invalid string
    with pytest.raises(Exception) as excinfo:
        field.validate("abc")
    assert "pattern" in str(excinfo.value)
