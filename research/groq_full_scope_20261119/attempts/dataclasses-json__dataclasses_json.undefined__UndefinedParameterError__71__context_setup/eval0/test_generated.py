import pytest
from dataclasses_json.undefined import UndefinedParameterError
from marshmallow.exceptions import ValidationError


def test_undefined_parameter_error_inherits_validation_error():
    """The custom error should be a subclass of marshmallow's ValidationError."""
    err = UndefinedParameterError("test message")
    assert isinstance(err, ValidationError)
    assert isinstance(err, UndefinedParameterError)


def test_undefined_parameter_error_message_handling():
    """The error should store the message passed to its constructor."""
    msg = "An undefined parameter was encountered."
    err = UndefinedParameterError(msg)
    # ValidationError stores the message in the `messages` attribute as a list
    assert err.messages == [msg]
    # The string representation should contain the message
    assert str(err) == msg


def test_undefined_parameter_error_with_complex_message():
    """The error should accept list or dict messages and preserve them."""
    complex_msg = {"field": ["missing", "invalid"], "global": ["error"]}

    err = UndefinedParameterError(complex_msg)
    # ValidationError stores the message in the `messages` attribute
    assert err.messages == [complex_msg]
    # The string representation should include the dict representation
    assert str(err) == str(complex_msg)
