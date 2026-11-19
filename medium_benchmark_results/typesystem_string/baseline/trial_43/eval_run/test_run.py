import pytest
from typesystem.fields import String

def test_string_validate_allow_blank_none_returns_empty_string():
    # When allow_blank is True and no default is provided, the field should default to an empty string
    field = String(allow_blank=True)
    assert field.default == ""

    # Validating a None value should return an empty string due to allow_blank and coerce_types
    result = field.validate(None)
    assert result == ""
