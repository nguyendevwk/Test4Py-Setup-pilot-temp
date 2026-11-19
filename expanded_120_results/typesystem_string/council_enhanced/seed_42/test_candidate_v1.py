import pytest
from typesystem.fields import String
from typesystem.exceptions import ValidationError


def test_string_validate_various_cases():
    s = String(
        max_length=5,
        min_length=2,
        pattern=r"^\w+$",
        allow_blank=True,
        trim_whitespace=True,
        coerce_types=True,
    )

    # None should be coerced to an empty string when allow_blank is True
    assert s.validate(None) == ""

    # Leading/trailing whitespace is stripped
    assert s.validate("  abc  ") == "abc"

    # Null character is removed
    assert s.validate("a\0b") == "ab"

    # Too short raises a min_length ValidationError
    with pytest.raises(ValidationError) as excinfo:
        s.validate("a")
    assert excinfo.value.code == "min_length"

    # Too long raises a max_length ValidationError
    with pytest.raises(ValidationError) as excinfo:
        s.validate("abcdef")
    assert excinfo.value.code == "max_length"

    # Pattern mismatch raises a pattern ValidationError
    with pytest.raises(ValidationError) as excinfo:
        s.validate("abc!")
    assert excinfo.value.code == "pattern"

    # Valid value passes unchanged
    assert s.validate("abc") == "abc"
