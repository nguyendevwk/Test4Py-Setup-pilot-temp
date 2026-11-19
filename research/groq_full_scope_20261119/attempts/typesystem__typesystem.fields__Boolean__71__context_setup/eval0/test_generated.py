import pytest
from typesystem.fields import Boolean

def test_boolean_coerce_and_allow_null():
    # Boolean with default coercion enabled and allow_null=True
    field = Boolean(allow_null=True, coerce_types=True)
    # True string should coerce to True
    assert field.validate("true") is True
    # False string should coerce to False
    assert field.validate("false") is False
    # Empty string should coerce to False
    assert field.validate("") is False
    # Null string should return None because allow_null is True
    assert field.validate("null") is None
    # None value should return None because allow_null is True
    assert field.validate(None) is None

def test_boolean_no_coerce_and_invalid_type():
    # Boolean with coercion disabled
    field = Boolean(coerce_types=False, allow_null=False)
    # Passing a non-boolean should raise ValidationError
    with pytest.raises(Exception) as excinfo:
        field.validate("yes")
    # The exception should be a ValidationError with code "type"
    assert hasattr(excinfo.value, "code")
    assert excinfo.value.code == "type"

def test_boolean_invalid_value_and_error_message():
    # Boolean with default settings
    field = Boolean()
    # Passing an unsupported value should raise ValidationError
    with pytest.raises(Exception) as excinfo:
        field.validate("unsupported")
    # The error message should match the defined error text
    assert str(excinfo.value) == "Must be a boolean."
