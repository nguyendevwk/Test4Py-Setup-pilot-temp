import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError

def test_undefined_parameter_error_inherits_validation_error():
    """The custom error should be a subclass of marshmallow's ValidationError."""
    assert issubclass(UndefinedParameterError, ValidationError)

def test_undefined_parameter_error_message_and_args():
    """Instantiating the error should store the message in its args."""
    msg = "Missing required field"
    err = UndefinedParameterError(message=msg)
    # The ValidationError base class stores the message in args[0]
    assert err.args[0] == msg
    # The error should be truthy and printable
    assert str(err) == msg

def test_raising_and_catching_undefined_parameter_error():
    """Raising the error should be catchable as ValidationError."""
    with pytest.raises(UndefinedParameterError) as excinfo:
        raise UndefinedParameterError(message="Error occurred")
    # The caught exception should be the same instance
    assert isinstance(excinfo.value, UndefinedParameterError)
    assert excinfo.value.args[0] == "Error occurred"
