import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError


def test_undefined_parameter_error_initialization():
    """The error should store the message and field_name correctly."""
    err = UndefinedParameterError("missing field", field_name="age")
    assert isinstance(err, UndefinedParameterError)
    # The message is stored in the first argument of args
    assert err.args[0] == "missing field"
    # The field_name attribute is set on the instance
    assert getattr(err, "field_name", None) == "age"


def test_undefined_parameter_error_inherits_validation_error():
    """UndefinedParameterError must be a subclass of marshmallow's ValidationError."""
    err = UndefinedParameterError("oops")
    assert isinstance(err, ValidationError)
    # ValidationError provides a `messages` attribute; it should be empty by default
    assert err.messages == {}


def test_undefined_parameter_error_can_be_raised_and_caught():
    """Raising the error should propagate correctly and be catchable."""
    with pytest.raises(UndefinedParameterError) as excinfo:
        raise UndefinedParameterError("error occurred", field_name="name")
    exc = excinfo.value
    assert exc.args[0] == "error occurred"
    assert exc.field_name == "name"
