import pytest
from typesystem.fields import Boolean
from typesystem import ValidationError

def test_boolean_accepts_bool_and_coerces_valid_strings():
    field = Boolean()
    # True and False are accepted as-is
    assert field.validate(True) is True
    assert field.validate(False) is False
    # Valid string representations are coerced to bool
    assert field.validate("true") is True
    assert field.validate("False") is False
    assert field.validate("ON") is True
    assert field.validate("off") is False
    assert field.validate("1") is True
    assert field.validate("0") is False
    # Empty string coerces to False
    assert field.validate("") is False

def test_boolean_null_handling_and_coerce_types_flag():
    # When allow_null is True, None is accepted
    field = Boolean(allow_null=True)
    assert field.validate(None) is None
    # When allow_null is True, null-like strings become None
    assert field.validate("null") is None
    assert field.validate("none") is None
    # When coerce_types is False, non-bool values raise an error
    field_no_coerce = Boolean(coerce_types=False, allow_null=True)
    with pytest.raises(ValidationError) as excinfo:
        field_no_coerce.validate("true")
    assert "Must be a boolean." in str(excinfo.value)

def test_boolean_invalid_inputs_raise_error():
    field = Boolean()
    # Non-bool, non-string, non-coercible values raise an error
    with pytest.raises(ValidationError) as excinfo:
        field.validate(3.14)
    assert "Must be a boolean." in str(excinfo.value)
    # Strings not in coerce_values raise an error
    with pytest.raises(ValidationError) as excinfo:
        field.validate("yes")
    assert "Must be a boolean." in str(excinfo.value)
    # None when allow_null is False raises an error
    with pytest.raises(ValidationError) as excinfo:
        field.validate(None)
    assert "May not be null." in str(excinfo.value)
