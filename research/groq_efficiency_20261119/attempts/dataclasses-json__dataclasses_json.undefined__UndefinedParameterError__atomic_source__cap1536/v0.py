import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError

def test_undefined_parameter_error_inherits_validation_error():
    """The custom error should inherit from marshmallow's ValidationError."""
    err = UndefinedParameterError("test message")
    assert isinstance(err, ValidationError)
    assert isinstance(err, UndefinedParameterError)

def test_error_message_and_args():
    """The error should store the message and args correctly."""
    msg = "Parameter 'foo' is undefined."
    err = UndefinedParameterError(msg)
    # ValidationError stores messages in the 'messages' attribute
    assert err.messages == [msg]
    # The string representation should include the message
    assert str(err) == msg

def test_error_can_be_raised_and_caught():
    """Raising the error should propagate and be catchable."""
    def raise_error():
        raise UndefinedParameterError("missing param")

    with pytest.raises(UndefinedParameterError) as excinfo:
        raise_error()
    assert excinfo.value.messages == ["missing param"]
