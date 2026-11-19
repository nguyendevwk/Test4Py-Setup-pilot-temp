import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError

def test_undefined_parameter_error_inherits_validation_error():
    """UndefinedParameterError should be a subclass of ValidationError."""
    err = UndefinedParameterError("test message")
    assert isinstance(err, ValidationError)
    assert isinstance(err, UndefinedParameterError)

def test_undefined_parameter_error_message_handling():
    """The error should store the provided message correctly."""
    msg = ["field1", "field2"]
    err = UndefinedParameterError(msg)
    # ValidationError stores the message in the `messages` attribute
    assert err.messages == msg
    # The string representation should include the message
    assert str(err) == str(msg)

def test_raising_and_catching_undefined_parameter_error():
    """Raising UndefinedParameterError should be catchable via pytest.raises."""
    with pytest.raises(UndefinedParameterError) as excinfo:
        raise UndefinedParameterError("error occurred")
    assert excinfo.value.messages == "error occurred"
