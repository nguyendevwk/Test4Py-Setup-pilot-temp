import pytest
from typesystem.fields import String
from typesystem.exceptions import ValidationError

def test_string_allow_blank_and_trim_and_constraints():
    s = String(allow_blank=True, trim_whitespace=True, max_length=5, min_length=2)
    assert s.default == ""

    # None and empty string are coerced to empty string when allow_blank is True
    assert s.validate(None) == ""
    assert s.validate("") == ""

    # Whitespace is trimmed by default
    assert s.validate("  abc  ") == "abc"

    # Exceeding max_length raises a ValidationError
    with pytest.raises(ValidationError) as excinfo:
        s.validate("abcdef")
    assert excinfo.value.code == "max_length"

    # Below min_length raises a ValidationError
    with pytest.raises(ValidationError) as excinfo:
        s.validate("a")
    assert excinfo.value.code == "min_length"

    # Non-string values raise a ValidationError
    with pytest.raises(ValidationError) as excinfo:
        s.validate(123)
    assert excinfo.value.code == "type"

    # Null characters are removed before validation
    assert s.validate("a\0b") == "ab"

    # Pattern validation
    sp = String(pattern=r'\d+')
    with pytest.raises(ValidationError) as excinfo:
        sp.validate("abc")
    assert excinfo.value.code == "pattern"
    assert sp.validate("123") == "123"
