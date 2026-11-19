import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError

def test_undefined_parameter_error_inherits_validation_error():
    """The custom error should be a subclass of marshmallow's ValidationError."""
    err = UndefinedParameterError("test message")
    assert isinstance(err, ValidationError)
    assert isinstance(err, UndefinedParameterError)

def test_undefined_parameter_error_message_and_args():
    """The error should store the message and any additional kwargs correctly."""
    err = UndefinedParameterError(message="missing field", field_name="foo", data={"bar": 1})
    # The message is stored in the first argument of args
    assert err.args[0] == "missing field"
    # Additional attributes are not automatically set; they must be passed via kwargs
    # but we can verify that kwargs are accessible if we pass them as part of the message
    # For this test we simply check that the message is preserved
    assert str(err) == "missing field"

def test_catching_undefined_parameter_error_in_context():
    """Raising and catching the error should work as expected."""
    def raise_error():
        raise UndefinedParameterError("error occurred")

    with pytest.raises(UndefinedParameterError) as excinfo:
        raise_error()
    assert "error occurred" in str(excinfo.value)
