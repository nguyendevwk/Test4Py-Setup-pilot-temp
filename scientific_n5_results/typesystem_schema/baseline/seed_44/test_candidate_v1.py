import pytest
from typesystem.schemas import Schema
from typesystem.fields import Field
from typesystem.exceptions import ValidationError, Message


class DummyField(Field):
    def __init__(self, *, read_only=False, default=None, **kwargs):
        super().__init__(**kwargs)
        self.read_only = read_only
        self._default = default

    def has_default(self):
        return self._default is not None

    def get_default_value(self):
        return self._default

    def validate_or_error(self, item):
        # Pass through the value without error
        return item, None


def test_schema_validate_applies_defaults_and_skips_read_only():
    schema = Schema(
        fields={
            "a": DummyField(),                 # required
            "b": DummyField(default=42),       # default applied
            "c": DummyField(read_only=True),   # skipped
        }
    )
    # Validate with only required field present
    validated = schema.validate({"a": "foo"})
    assert validated == {"a": "foo", "b": 42}
    assert "c" not in validated

    # Validate with read-only field present; it should be ignored
    validated_with_readonly = schema.validate({"a": "bar", "c": "ignored"})
    assert validated_with_readonly == {"a": "bar", "b": 42}
