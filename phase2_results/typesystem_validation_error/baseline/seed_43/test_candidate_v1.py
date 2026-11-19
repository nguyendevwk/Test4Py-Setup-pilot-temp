import pytest
from typesystem.base import ValidationError, BaseError

def test_validation_error_inheritance_and_message():
    msg = "Invalid data"
    err = ValidationError(msg)
    assert isinstance(err, BaseError)
    assert isinstance(err, Exception)
    assert str(err) == msg

    with pytest.raises(ValidationError) as excinfo:
        raise ValidationError("error")
    assert str(excinfo.value) == "error"
