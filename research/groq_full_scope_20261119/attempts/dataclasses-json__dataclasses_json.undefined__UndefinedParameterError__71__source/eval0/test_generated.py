import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError

def test_undefined_parameter_error_inherits_validation_error():
    """The custom error should be a subclass of marshmallow's ValidationError."""
    err = UndefinedParameterError("test message")
    assert isinstance(err, ValidationError)
    assert isinstance(err, UndefinedParameterError)

def test_error_message_and_args():
    """The error should store the message and args correctly."""
    msg = "Missing required field 'name'"
    err = UndefinedParameterError(msg)
    # ValidationError stores the message in the first element of args
    assert err.args[0] == msg
    # The string representation should include the message
    assert str(err) == msg

def test_error_can_be_raised_and_caught():
    """Raising the error should propagate and be catchable."""
    def raise_error():
        raise UndefinedParameterError("boom")

    with pytest.raises(UndefinedParameterError) as excinfo:
        raise_error()
    assert excinfo.value.args[0] == "boom"
