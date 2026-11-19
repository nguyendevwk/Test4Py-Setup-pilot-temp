import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError

def test_undefined_parameter_error_inherits_validation_error():
    """UndefinedParameterError should be a subclass of ValidationError."""
    assert issubclass(UndefinedParameterError, ValidationError)
    assert isinstance(UndefinedParameterError("msg"), ValidationError)

def test_undefined_parameter_error_message_and_args():
    """The error should store the message and args correctly."""
    msg = "parameter not defined"
    err = UndefinedParameterError(msg)
    assert err.args == (msg,)
    assert str(err) == msg

def test_raising_and_catching_undefined_parameter_error():
    """Raising UndefinedParameterError should be catchable as ValidationError."""
    with pytest.raises(ValidationError) as excinfo:
        raise UndefinedParameterError("missing field")
    assert isinstance(excinfo.value, UndefinedParameterError)
    assert str(excinfo.value) == "missing field"
