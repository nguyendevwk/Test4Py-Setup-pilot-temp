import pytest
import typesystem
from typesystem.base import ValidationError, BaseError

def test_validation_error_behavior():
    # Instantiation and inheritance
    err = ValidationError("Test error")
    assert isinstance(err, ValidationError)
    assert isinstance(err, BaseError)
    assert isinstance(err, Exception)
    assert err.args == ("Test error",)
    assert "Test error" in str(err)

    # Raising and catching
    with pytest.raises(ValidationError) as excinfo:
        raise ValidationError("Raised error")
    raised_err = excinfo.value
    assert isinstance(raised_err, ValidationError)
    assert raised_err.args == ("Raised error",)
    assert "Raised error" in str(raised_err)

    # Schema validation raises ValidationError on missing field
    class Person(typesystem.Schema):
        name = typesystem.String()
        age = typesystem.Integer()

    with pytest.raises(ValidationError) as excinfo2:
        Person.validate({"name": "Alice"})  # missing age
    schema_err = excinfo2.value
    assert isinstance(schema_err, ValidationError)
    assert isinstance(schema_err, BaseError)
    assert isinstance(schema_err, Exception)
    assert "age" in str(schema_err)

    # validate_or_error returns a ValidationError instance
    result = Person.validate_or_error({"name": "Alice"})
    assert isinstance(result, ValidationError)
    assert isinstance(result, BaseError)
    assert isinstance(result, Exception)
    assert "age" in str(result)
