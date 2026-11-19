import pytest
from typesystem.fields import Boolean
from typesystem.base import ValidationError

def test_boolean_coercion_and_allow_null():
    # Boolean field with default coerce_types=True and allow_null=False
    field = Boolean()
    # Valid boolean values pass unchanged
    assert field.validate(True) is True
    assert field.validate(False) is False
    # Coercible string values are converted to bool
    assert field.validate("true") is True
    assert field.validate("False") is False
    assert field.validate("on") is True
    assert field.validate("0") is False
    # Empty string coerces to False
    assert field.validate("") is False
    # Integer values coerced
    assert field.validate(1) is True
    assert field.validate(0) is False

def test_boolean_null_handling_and_coerce_null_values():
    # Boolean field with allow_null=True
    field = Boolean(allow_null=True)
    # None is allowed
    assert field.validate(None) is None
    # Coerce null-like values to None
    assert field.validate("") is None
    assert field.validate("null") is None
    assert field.validate("none") is None
    # Non-null values still validated
    assert field.validate("true") is True

def test_boolean_invalid_type_raises_error():
    # Boolean field with coerce_types=False should reject non-bool types
    field = Boolean(coerce_types=False)
    with pytest.raises(ValidationError) as excinfo:
        field.validate("yes")
    assert "Must be a boolean." in str(excinfo.value)
    # Even numeric values are rejected when coerce_types is False
    with pytest.raises(ValidationError):
        field.validate(1)
