import pytest
import typesystem
from typesystem.fields import Field
from typesystem.base import ValidationError, ValidationResult

# Helper subclass that implements validate simply returns the value
class DummyField(Field):
    def validate(self, value):
        return value

def test_default_value_callable_and_has_default():
    # default is a callable that returns a dynamic value
    def default_factory():
        return 42

    f = DummyField(default=default_factory)
    assert f.has_default() is True
    # get_default_value should call the factory each time
    assert f.get_default_value() == 42
    # Changing the factory result should reflect in get_default_value
    default_factory = lambda: 99
    f.default = default_factory
    assert f.get_default_value() == 99

def test_validation_error_text_and_validation_error():
    # Define a field with custom error messages
    class IntField(Field):
        errors = {"required": "Field '{title}' is required."}

        def validate(self, value):
            if value is None:
                raise self.validation_error("required")
            return int(value)

    f = IntField(title="age")
    # validate_or_error should return a ValidationResult with error
    result = f.validate_or_error(None)
    assert isinstance(result.error, ValidationError)
    assert result.error.code == "required"
    assert result.error.text == "Field 'age' is required."
    # get_error_text should format the message correctly
    assert f.get_error_text("required") == "Field 'age' is required."

def test_union_operator_combines_fields():
    # Create two dummy fields
    f1 = DummyField(title="first")
    f2 = DummyField(title="second")
    # Use the | operator to create a Union
    union = f1 | f2
    # The Union class is defined in typesystem.unique
    from typesystem.unique import Union
    assert isinstance(union, Union)
    # The Union should contain both fields
    assert set(union.any_of) == {f1, f2}
    # Combining with another Union should merge all fields
    f3 = DummyField(title="third")
    union2 = union | f3
    assert set(union2.any_of) == {f1, f2, f3}
