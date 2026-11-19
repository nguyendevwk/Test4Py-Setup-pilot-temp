import pytest
from typesystem.fields import String
from typesystem.base import ValidationError

def test_string_validates_and_trims_whitespace():
    field = String(trim_whitespace=True, allow_blank=False)
    # Leading/trailing whitespace should be removed
    assert field.validate("  hello  ") == "hello"
    # Empty string should raise blank error
    with pytest.raises(ValidationError) as excinfo:
        field.validate("")
    assert excinfo.value.code == "blank"

def test_string_length_and_pattern_constraints():
    field = String(min_length=3, max_length=5, pattern=r"^[a-z]+$", allow_blank=False)
    # Valid string within length and matching pattern
    assert field.validate("abc") == "abc"
    # Too short
    with pytest.raises(ValidationError) as excinfo:
        field.validate("ab")
    assert excinfo.value.code == "min_length"
    # Too long
    with pytest.raises(ValidationError) as excinfo:
        field.validate("abcdef")
    assert excinfo.value.code == "max_length"
    # Pattern mismatch
    with pytest.raises(ValidationError) as excinfo:
        field.validate("abc1")
    assert excinfo.value.code == "pattern"

def test_string_null_and_blank_handling():
    # allow_blank with default set to empty string
    field = String(allow_blank=True)
    assert field.has_default()
    assert field.get_default_value() == ""
    # None is allowed when allow_null is True
    field.allow_null = True
    assert field.validate(None) is None
    # None is coerced to empty string when allow_blank and coerce_types
    field.allow_null = False
    assert field.validate(None) == ""
    # None not allowed and not blank
    field.allow_blank = False
    with pytest.raises(ValidationError) as excinfo:
        field.validate(None)
    assert excinfo.value.code == "null"
