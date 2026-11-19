import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError

def test_undefined_parameter_error_is_validation_error():
    """The custom error should inherit from marshmallow's ValidationError."""
    err = UndefinedParameterError("test message")
    assert isinstance(err, ValidationError)
    assert isinstance(err, UndefinedParameterError)

def test_undefined_parameter_error_message():
    """The error should preserve the message passed to it."""
    message = "Undefined parameter encountered"
    err = UndefinedParameterError(message)
    assert str(err) == message

def test_raising_undefined_parameter_error():
    """Raising the error should propagate correctly and be caught by pytest.raises."""
    with pytest.raises(UndefinedParameterError) as excinfo:
        raise UndefinedParameterError("boom")
    assert str(excinfo.value) == "boom"
