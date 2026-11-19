import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError

def test_undefined_parameter_error_inherits_validation_error():
    """UndefinedParameterError should be a subclass of marshmallow's ValidationError."""
    assert issubclass(UndefinedParameterError, ValidationError)

def test_undefined_parameter_error_message_and_args():
    """Instantiating with a message should store it correctly and expose args."""
    msg = "Parameter 'foo' is undefined."
    err = UndefinedParameterError(msg)
    assert isinstance(err, UndefinedParameterError)
    assert err.args == (msg,)
    assert str(err) == msg

def test_undefined_parameter_error_with_multiple_arguments():
    """The error should accept multiple arguments and preserve them in args."""
    msg1 = "Missing field."
    msg2 = "Check schema."
    err = UndefinedParameterError(msg1, msg2)
    assert err.args == (msg1, msg2)
    # The string representation joins args with spaces
    assert str(err) == f"{msg1} {msg2}"
