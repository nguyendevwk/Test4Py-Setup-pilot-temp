import pytest
from typesystem.fields import String

def test_string_validate_null_coerced_to_empty_when_allow_blank_and_coerce_types():
    """When allow_blank and coerce_types are True, validate(None) should return an empty string."""
    field = String(allow_blank=True, coerce_types=True)
    result = field.validate(None)
    assert result == "", "Expected empty string when null is coerced"
    assert isinstance(result, str), "Result should be a string instance"
