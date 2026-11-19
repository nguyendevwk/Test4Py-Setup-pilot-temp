import pytest
from typesystem.fields import Boolean
from typesystem import ValidationError

def test_boolean_coercion_and_null_handling():
    # Boolean field with default coercion enabled
    field = Boolean()
    # Valid boolean values pass unchanged
    assert field.validate(True) is True
    assert field.validate(False) is False
    # String representations are coerced to booleans
    assert field.validate("true") is True
    assert field.validate("False") is False
    assert field.validate("ON") is True
    assert field.validate("off") is False
    # Numeric representations are coerced
    assert field.validate(1) is True
    assert field.validate(0) is False
    # Empty string coerces to False
    assert field.validate("") is False

def test_boolean_null_coercion_and_allow_null():
    # Boolean field that allows null values
    field = Boolean(allow_null=True)
    # None is allowed and returned unchanged
    assert field.validate(None) is None
    # Null string representations are coerced to None
    assert field.validate("null") is None
    assert field.validate("none") is None
    assert field.validate("") is None
    # Non-null values still coerced normally
    assert field.validate("true") is True

def test_boolean_invalid_input_raises_error():
    # Boolean field with coercion disabled
    field = Boolean(coerce_types=False)
    # Non-boolean, non-string input raises ValidationError
    with pytest.raises(ValidationError) as excinfo:
        field.validate(3.14)
    assert "Must be a boolean." in str(excinfo.value)

    # String not in coerce_values raises ValidationError
    with pytest.raises(ValidationError) as excinfo:
        field.validate("maybe")
    assert "Must be a boolean." in str(excinfo.value)
