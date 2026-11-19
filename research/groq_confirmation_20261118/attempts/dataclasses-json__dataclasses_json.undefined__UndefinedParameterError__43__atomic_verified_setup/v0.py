import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError

def test_undefined_parameter_error_inherits_validation_error():
    """The custom error should be a subclass of marshmallow's ValidationError."""
    err = UndefinedParameterError("test message")
    assert isinstance(err, ValidationError)
    assert isinstance(err, UndefinedParameterError)
    assert err.args == ("test message",)

def test_error_message_and_kwargs():
    """The error should preserve the message and any additional keyword arguments."""
    err = UndefinedParameterError("missing field", field_name="age", data={"name": "Alice"})
    # The message is stored in args[0]
    assert err.args[0] == "missing field"
    # Additional kwargs are stored in the error's `kwargs` attribute
    assert getattr(err, "kwargs", {}) == {"field_name": "age", "data": {"name": "Alice"}}

def test_raising_and_catching_error():
    """Raising the error should be catchable and provide the correct message."""
    with pytest.raises(UndefinedParameterError) as excinfo:
        raise UndefinedParameterError("invalid input", field_name="email")
    exc = excinfo.value
    assert exc.args[0] == "invalid input"
    assert exc.kwargs == {"field_name": "email"}
