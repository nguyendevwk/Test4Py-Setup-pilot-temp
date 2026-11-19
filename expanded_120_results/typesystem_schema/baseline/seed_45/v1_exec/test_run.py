import pytest
from typesystem.schemas import Schema, ValidationError, Message

class DummyField:
    """Minimal Field implementation for testing Schema."""
    def __init__(self, *, read_only=False, default=None):
        self.read_only = read_only
        self._default = default

    def has_default(self):
        return self._default is not None

    def get_default_value(self):
        return self._default

    def validate_or_error(self, value):
        # Accept any value without error
        return value, None

    def serialize(self, value):
        return value

def test_schema_validate_missing_required_and_defaults_and_read_only():
    schema = Schema(
        fields={
            "a": DummyField(),                # required
            "b": DummyField(default=5),       # optional with default
            "c": DummyField(read_only=True),  # read-only, ignored
        }
    )

    # Missing required field 'a' should raise ValidationError with code 'required'
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"b": 10})
    error_codes = [msg.code for msg in excinfo.value.messages]
    assert "required" in error_codes
    assert any(msg.index == ["a"] for msg in excinfo.value.messages)

    # Providing required field yields validated dict with defaults applied
    validated = schema.validate({"a": 1})
    assert validated == {"a": 1, "b": 5}

    # Read-only field is ignored even if present in input
    validated = schema.validate({"a": 2, "c": 3})
    assert validated == {"a": 2, "b": 5}
