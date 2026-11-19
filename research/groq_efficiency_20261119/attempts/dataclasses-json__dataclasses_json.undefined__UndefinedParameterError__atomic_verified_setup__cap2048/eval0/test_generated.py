import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError

def test_undefined_parameter_error_inherits_validation_error():
    """The custom error should be a subclass of marshmallow's ValidationError."""
    err = UndefinedParameterError("test message")
    assert isinstance(err, ValidationError)
    assert isinstance(err, UndefinedParameterError)

def test_undefined_parameter_error_message_and_args():
    """The error should store the message and any additional kwargs correctly."""
    err = UndefinedParameterError(message="missing field", field_name="name", data={"name": None})
    # The message is stored in the first argument of args
    assert err.args[0] == "missing field"
    # The original kwargs are accessible via the error's __dict__
    assert err.field_name == "name"
    assert err.data == {"name": None}

def test_raising_and_catching_undefined_parameter_error():
    """Raising the error should propagate and be catchable as ValidationError."""
    def raise_error():
        raise UndefinedParameterError("error occurred", field_name="age")

    with pytest.raises(UndefinedParameterError) as excinfo:
        raise_error()
    # The caught exception should have the correct message
    assert str(excinfo.value) == "error occurred"
    # It should also be catchable as the base ValidationError
    with pytest.raises(ValidationError):
        raise_error()
