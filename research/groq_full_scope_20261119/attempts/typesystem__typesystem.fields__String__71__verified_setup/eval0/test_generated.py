import pytest
from typesystem.fields import String
from typesystem import ValidationError


def test_trim_whitespace_and_blank_behavior():
    """String field should trim whitespace and raise a blank error when not allowed."""
    field = String(allow_blank=False, trim_whitespace=True)
    # Value with only whitespace should be trimmed to empty and raise a blank error
    with pytest.raises(ValidationError) as excinfo:
        field.validate("   ")
    assert "blank" in str(excinfo.value)

    # Value with non‑blank content should be trimmed correctly
    result = field.validate("  hello  ")
    assert result == "hello"


def test_max_length_boundary():
    """String field should enforce max_length correctly."""
    field = String(max_length=5)
    # Exactly at the boundary should pass
    assert field.validate("abcde") == "abcde"

    # Exceeding the boundary should raise a ValidationError
    with pytest.raises(ValidationError) as excinfo:
        field.validate("abcdef")
    assert "max_length" in str(excinfo.value)


def test_pattern_and_null_coercion():
    """String field should enforce regex patterns and coerce null to empty string when allowed."""
    field = String(pattern=r"\d+", allow_blank=True, coerce_types=True)
    # Valid numeric string passes
    assert field.validate("12345") == "12345"

    # Non‑numeric string fails pattern validation
    with pytest.raises(ValidationError) as excinfo:
        field.validate("abc")
    assert "pattern" in str(excinfo.value)

    # None should be coerced to an empty string because allow_blank is True
    assert field.validate(None) == ""
