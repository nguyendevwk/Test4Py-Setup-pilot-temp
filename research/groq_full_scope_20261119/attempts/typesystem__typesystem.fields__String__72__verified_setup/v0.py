import pytest
from typesystem import String, ValidationError

# Test normal validation: string passes all constraints
def test_string_validates_correctly():
    field = String(max_length=10, min_length=3, pattern=r"^\w+$", allow_blank=False)
    result = field.validate("abc123")
    assert result == "abc123"

# Test boundary conditions: trimming, null character removal, and length limits
def test_string_boundary_conditions():
    field = String(max_length=5, trim_whitespace=True, allow_blank=True)
    # Leading/trailing whitespace should be stripped
    assert field.validate("  abc  ") == "abc"
    # Null character should be removed
    assert field.validate("a\0b") == "ab"
    # Value exactly at max_length passes
    assert field.validate("abcde") == "abcde"
    # Value exceeding max_length raises ValidationError
    with pytest.raises(ValidationError) as excinfo:
        field.validate("abcdef")
    assert "max_length" in str(excinfo.value)

# Test error handling: null, blank, type, and pattern mismatches
def test_string_error_cases():
    field = String(allow_blank=False, coerce_types=True)
    # None value when not allowed should raise
    with pytest.raises(ValidationError) as excinfo:
        field.validate(None)
    assert "null" in str(excinfo.value)

    # Empty string when blank not allowed should raise
    with pytest.raises(ValidationError) as excinfo:
        field.validate("")
    assert "blank" in str(excinfo.value)

    # Non-string type should raise
    with pytest.raises(ValidationError) as excinfo:
        field.validate(123)
    assert "type" in str(excinfo.value)

    # Pattern mismatch should raise
    field_with_pattern = String(pattern=r"^\d+$")
    with pytest.raises(ValidationError) as excinfo:
        field_with_pattern.validate("abc")
    assert "pattern" in str(excinfo.value)
