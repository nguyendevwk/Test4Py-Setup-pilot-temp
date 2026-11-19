import pytest
from typesystem.fields import Boolean
from typesystem import ValidationError

def test_boolean_coercion_and_null_handling():
    # Boolean field with default coercion enabled
    field = Boolean()
    # Valid boolean values pass through unchanged
    assert field.validate(True) is True
    assert field.validate(False) is False
    # String representations are coerced to bool
    assert field.validate("true") is True
    assert field.validate("false") is False
    assert field.validate("on") is True
    assert field.validate("off") is False
    assert field.validate("1") is True
    assert field.validate("0") is False
    # Empty string coerces to False
    assert field.validate("") is False
    # Integer representations are coerced
    assert field.validate(1) is True
    assert field.validate(0) is False
    # Null values raise ValidationError when allow_null is False
    with pytest.raises(ValidationError) as excinfo:
        field.validate(None)
    assert "null" in str(excinfo.value)

def test_boolean_null_coercion_allowed():
    # Boolean field with allow_null=True and coercion enabled
    field = Boolean(allow_null=True)
    # Null values return None
    assert field.validate(None) is None
    # Coerce null-like strings to None
    assert field.validate("") is None
    assert field.validate("null") is None
    assert field.validate("none") is None
    # Non-null strings still coerced to bool
    assert field.validate("true") is True
    assert field.validate("false") is False

def test_boolean_type_error_when_coercion_disabled():
    # Boolean field with coercion disabled
    field = Boolean(coerce_types=False, allow_null=True)
    # Passing a non-boolean raises ValidationError
    with pytest.raises(ValidationError) as excinfo:
        field.validate("true")
    assert "type" in str(excinfo.value)
    # Passing a boolean still works
    assert field.validate(True) is True
    # Passing None returns None because allow_null=True
    assert field.validate(None) is None
