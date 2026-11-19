import pytest
from typesystem.fields import Boolean

def test_boolean_coercion_and_null_handling(tmp_path):
    # Boolean with default coercion enabled
    field = Boolean(allow_null=True)
    # Valid boolean stays unchanged
    assert field.validate(True) is True
    assert field.validate(False) is False
    # String representations are coerced to bool
    assert field.validate("true") is True
    assert field.validate("False") is False
    assert field.validate("ON") is True
    assert field.validate("off") is False
    assert field.validate("1") is True
    assert field.validate("0") is False
    # Empty string coerces to False
    assert field.validate("") is False
    # Null values are allowed and returned as None
    assert field.validate(None) is None
    # Null string values are coerced to None when allow_null is True
    assert field.validate("null") is None
    assert field.validate("none") is None

def test_boolean_type_error_when_coercion_disabled(tmp_path):
    # Boolean with coercion disabled
    field = Boolean(coerce_types=False, allow_null=True)
    # Passing a non-boolean raises a ValidationError with code "type"
    with pytest.raises(Exception) as excinfo:
        field.validate("true")
    assert "Must be a boolean." in str(excinfo.value)
    # Passing None is still allowed
    assert field.validate(None) is None

def test_boolean_null_error_when_not_allowed(tmp_path):
    # Boolean with null not allowed
    field = Boolean(allow_null=False)
    # Passing None raises a ValidationError with code "null"
    with pytest.raises(Exception) as excinfo:
        field.validate(None)
    assert "May not be null." in str(excinfo.value)
    # Passing a valid boolean still works
    assert field.validate(True) is True
