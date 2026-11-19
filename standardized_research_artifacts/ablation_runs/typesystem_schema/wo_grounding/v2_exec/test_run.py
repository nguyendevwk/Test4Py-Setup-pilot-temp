import pytest
from typesystem.schemas import Schema, ValidationError, Field


class DummyField(Field):
    def __init__(self, *, read_only=False, default=None, allow_null=False):
        super().__init__(allow_null=allow_null)
        self.read_only = read_only
        self._default = default

    def has_default(self):
        return self._default is not None

    def get_default_value(self):
        return self._default

    def validate_or_error(self, value):
        return value, None

    def serialize(self, value):
        return value


def test_schema_missing_required_raises_validation_error():
    schema = Schema(fields={"a": DummyField(), "b": DummyField(default=5)})
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"b": 5})
    error = excinfo.value
    assert any(msg.code == "required" and msg.index == ["a"] for msg in error.messages())
