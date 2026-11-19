import re
import pytest
from typesystem.fields import String
from typesystem import ValidationError

def test_string_valid_and_trim_and_null_coercion():
    # allow_blank True, trim_whitespace True, coerce_types True
    field = String(allow_blank=True, trim_whitespace=True, coerce_types=True)
    # Leading/trailing whitespace should be stripped
    assert field.validate("  hello  ") == "hello"
    # Null should be coerced to empty string because allow_blank
    assert field.validate(None) == ""
    # Empty string should be allowed because allow_blank
    assert field.validate("") == ""
    # Non-string should raise type error
    with pytest.raises(ValidationError) as excinfo:
        field.validate(123)
    assert "type" in str(excinfo.value)

def test_string_length_constraints():
    # max_length 5, min_length 3
    field = String(max_length=5, min_length=3)
    # Valid length
    assert field.validate("abc") == "abc"
    # Too short
    with pytest.raises(ValidationError) as excinfo:
        field.validate("ab")
    assert "min_length" in str(excinfo.value)
    # Too long
    with pytest.raises(ValidationError) as excinfo:
        field.validate("abcdef")
    assert "max_length" in str(excinfo.value)

def test_string_pattern_and_format():
    # pattern must match digits only
    field = String(pattern=r"^\d+$")
    # Valid pattern
    assert field.validate("12345") == "12345"
    # Invalid pattern
    with pytest.raises(ValidationError) as excinfo:
        field.validate("abc")
    assert "pattern" in str(excinfo.value)
    # Format email: should validate using built-in format
    email_field = String(format="email")
    assert email_field.validate("user@example.com") == "user@example.com"
    with pytest.raises(ValidationError) as excinfo:
        email_field.validate("not-an-email")
    assert "format" in str(excinfo.value)
