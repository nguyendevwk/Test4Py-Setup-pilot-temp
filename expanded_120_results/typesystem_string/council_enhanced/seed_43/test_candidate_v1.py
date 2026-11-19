import pytest
from typesystem.fields import String
from typesystem.exceptions import ValidationError

def test_string_validate_behavior():
    s = String(
        allow_blank=True,
        trim_whitespace=True,
        min_length=3,
        max_length=5,
        pattern=r"^[a-z]+$",
        coerce_types=True,
    )
    assert s.default == ""
    assert s.validate(None) == ""
    assert s.validate("  abc  ") == "abc"
    with pytest.raises(ValidationError):
        s.validate("ab")
    with pytest.raises(ValidationError):
        s.validate("abcdef")
    with pytest.raises(ValidationError):
        s.validate("abc1")
    with pytest.raises(ValidationError):
        s.validate("abc\0def")
    assert s.validate("") == ""
    assert s.validate("   ") == ""
    assert s.validate("   abc   ") == "abc"

    s2 = String(allow_blank=True, coerce_types=False)
    with pytest.raises(ValidationError):
        s2.validate(None)
