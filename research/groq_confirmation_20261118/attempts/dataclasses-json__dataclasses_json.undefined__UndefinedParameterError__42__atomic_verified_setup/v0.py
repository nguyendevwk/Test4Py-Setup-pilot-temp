import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError


def test_undefined_parameter_error_inherits_validation_error():
    """UndefinedParameterError should be a subclass of ValidationError."""
    err = UndefinedParameterError("test message")
    assert isinstance(err, ValidationError)
    assert isinstance(err, UndefinedParameterError)


def test_error_message_and_attributes():
    """The error should store the message and optional field_name correctly."""
    err = UndefinedParameterError("missing field", field_name="age")
    # The message is stored in the args tuple
    assert err.args[0] == "missing field"
    # The field_name attribute is set on the instance
    assert getattr(err, "field_name", None) == "age"
    # The default field_name should be None if not provided
    err_default = UndefinedParameterError("no field")
    assert getattr(err_default, "field_name", None) is None


def test_error_can_be_raised_and_caught_with_pytest_raises():
    """Raising UndefinedParameterError should be catchable with pytest.raises."""
    with pytest.raises(UndefinedParameterError) as excinfo:
        raise UndefinedParameterError("error occurred", field_name="name")
    # Verify the exception message and field_name in the caught exception
    assert str(excinfo.value) == "error occurred"
    assert excinfo.value.field_name == "name"
