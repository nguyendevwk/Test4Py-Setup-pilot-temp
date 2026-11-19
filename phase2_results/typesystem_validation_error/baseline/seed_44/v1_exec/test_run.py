import pytest
from typesystem.base import ValidationError, BaseError

def test_validation_error_attributes_and_str():
    errors = ["error1", "error2"]
    message = "Custom validation error"

    # Instantiate with explicit message
    e = ValidationError(errors, message=message)
    assert isinstance(e, ValidationError)
    assert isinstance(e, BaseError)
    assert e.errors == errors
    assert e.message == message
    assert str(e) == message

    # Instantiate with default message
    e_default = ValidationError(errors)
    assert e_default.errors == errors
    assert e_default.message is not None
    assert str(e_default) == e_default.message

    # Raising and catching the exception
    with pytest.raises(ValidationError) as excinfo:
        raise ValidationError(errors, message=message)
    assert excinfo.value.errors == errors
    assert str(excinfo.value) == message
