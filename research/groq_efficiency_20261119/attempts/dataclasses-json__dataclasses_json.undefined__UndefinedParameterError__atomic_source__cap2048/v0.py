import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError

def test_undefined_parameter_error_inherits_validation_error():
    """The custom error should be a subclass of marshmallow's ValidationError."""
    err = UndefinedParameterError("test message")
    assert isinstance(err, ValidationError)
    assert isinstance(err, UndefinedParameterError)

def test_error_message_and_args():
    """The error should store the provided message correctly."""
    msg = "Undefined parameter encountered"
    err = UndefinedParameterError(msg)
    # ValidationError stores messages in the `messages` attribute as a list
    assert err.messages == [msg]
    # The string representation should include the message
    assert str(err) == msg

def test_raising_and_catching_error():
    """Raising the error should be catchable and preserve the message."""
    def raise_error():
        raise UndefinedParameterError("boom")

    with pytest.raises(UndefinedParameterError) as excinfo:
        raise_error()
    assert excinfo.value.messages == ["boom"]
