import pytest
from typesystem.schemas import Schema
from typesystem.fields import Field, ValidationError


class DummyField(Field):
    """A minimal Field that always returns the input value and can have a default."""

    def validate(self, value):
        return value


def test_schema_validate_required_and_readonly():
    # Field 'a' has a default, so it is not required.
    # Field 'b' is read-only, so it is ignored during validation.
    # Field 'c' has no default and is not read-only, so it is required.
    schema = Schema(
        fields={
            "a": DummyField(default=1),
            "b": DummyField(read_only=True),
            "c": DummyField(),
        }
    )

    # Validate with only 'a' provided: should raise a ValidationError for missing 'c'.
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"a": 42})
    error = excinfo.value
    # There should be exactly one error message with code 'required' and index ['c'].
    assert len(error.messages) == 1
    msg = error.messages[0]
    assert msg.code == "required"
    assert msg.index == ["c"]

    # Validate with all required fields provided: should succeed and return a dict
    # containing only non-read-only fields.
    result = schema.validate({"a": 42, "c": 99})
    assert result == {"a": 42, "c": 99}
    # Read-only field 'b' should not appear in the validated output.
    assert "b" not in result
