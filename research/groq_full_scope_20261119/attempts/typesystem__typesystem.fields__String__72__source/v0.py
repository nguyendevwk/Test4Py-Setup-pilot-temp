import re
import pytest
from typesystem.fields import String
from typesystem.exceptions import ValidationError

# Test 1: Normal validation with trimming and default handling
def test_string_validate_normal():
    field = String(allow_blank=False, trim_whitespace=True, min_length=3, max_length=10)
    # Leading/trailing whitespace should be stripped
    assert field.validate("  hello  ") == "hello"
    # Value within bounds passes
    assert field.validate("world") == "world"
    # Empty string should raise blank error
    with pytest.raises(ValidationError) as excinfo:
        field.validate("")
    assert "blank" in str(excinfo.value)

# Test 2: Boundary conditions for min_length and max_length
def test_string_validate_boundaries():
    field = String(min_length=5, max_length=5)
    # Exactly at min_length and max_length
    assert field.validate("abcde") == "abcde"
    # Below min_length
    with pytest.raises(ValidationError) as excinfo_min:
        field.validate("abcd")
    assert "min_length" in str(excinfo_min.value)
    # Above max_length
    with pytest.raises(ValidationError) as excinfo_max:
        field.validate("abcdef")
    assert "max_length" in str(excinfo_max.value)

# Test 3: Pattern matching and null character handling
def test_string_validate_pattern_and_null_char():
    pattern = r"^[A-Z]+$"
    field = String(pattern=pattern, allow_blank=False)
    # Valid pattern
    assert field.validate("ABC") == "ABC"
    # Invalid pattern
    with pytest.raises(ValidationError) as excinfo:
        field.validate("Abc")
    assert "pattern" in str(excinfo.value)
    # Null character should be removed
    assert field.validate("A\0B") == "AB"
