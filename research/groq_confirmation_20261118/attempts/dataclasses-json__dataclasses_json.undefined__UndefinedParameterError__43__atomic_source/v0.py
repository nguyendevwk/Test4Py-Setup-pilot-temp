import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError

def test_undefined_parameter_error_inherits_validation_error():
    """The custom error should be a subclass of marshmallow's ValidationError."""
    err = UndefinedParameterError("test message")
    assert isinstance(err, ValidationError)
    assert isinstance(err, UndefinedParameterError)

def test_error_message_and_args():
    """The error should store the provided message and args correctly."""
    msg = "Undefined parameter encountered"
    err = UndefinedParameterError(msg, 42, key="value")
    # ValidationError stores message in `message` attribute
    assert err.message == msg
    # The args tuple should contain the message and any additional arguments
    assert err.args[0] == msg
    assert err.args[1] == 42
    assert err.args[2] == ("key", "value")

def test_error_raised_and_caught():
    """Raising the error should propagate and be catchable as ValidationError."""
    def func():
        raise UndefinedParameterError("boom")
    with pytest.raises(UndefinedParameterError) as excinfo:
        func()
    assert str(excinfo.value) == "boom"
    # Also catchable as the base class
    with pytest.raises(ValidationError):
        func()
