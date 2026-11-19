import pytest
from typesystem.fields import String

def test_string_validate_behavior():
    field = String(
        allow_blank=True,
        trim_whitespace=True,
        min_length=3,
        max_length=5,
        pattern=r'\d+',
    )
    # None coerces to empty string when allow_blank is True
    assert field.validate(None) == ""
    # Valid string with whitespace trimmed
    assert field.validate("  123  ") == "123"
    # Too short string triggers min_length error
    with pytest.raises(Exception):
        field.validate("12")
    # Too long string triggers max_length error
    with pytest.raises(Exception):
        field.validate("123456")
    # Pattern mismatch triggers pattern error
    with pytest.raises(Exception):
        field.validate("abc")
    # Null character is removed before validation
    assert field.validate("a\0bc") == "abc"
    # Blank string not allowed when allow_blank is False
    field_no_blank = String(allow_blank=False, trim_whitespace=True)
    with pytest.raises(Exception):
        field_no_blank.validate("   ")
