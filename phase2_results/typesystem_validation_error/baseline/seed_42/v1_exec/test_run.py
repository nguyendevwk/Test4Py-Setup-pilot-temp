import pytest
from typesystem.base import ValidationError, BaseError

def test_validation_error_inheritance_and_message():
    # Instantiation should preserve the message and inherit from BaseError
    e = ValidationError("sample error")
    assert isinstance(e, BaseError)
    assert str(e) == "sample error"

    # Raising and catching should yield the same message
    with pytest.raises(ValidationError) as excinfo:
        raise ValidationError("raised error")
    assert str(excinfo.value) == "raised error"
