import pytest
from typesystem.schemas import Schema, Field, ValidationError


class DummyField(Field):
    def __init__(self, *, default=None, read_only=False, allow_null=False, **kwargs):
        super().__init__(**kwargs)
        self._default = default
        self.read_only = read_only
        self.allow_null = allow_null

    def has_default(self):
        return self._default is not None

    def get_default_value(self):
        return self._default

    def validate_or_error(self, value):
        return value, None

    def serialize(self, value):
        return value


def test_schema_validate_required_and_default_and_invalid_key():
    schema = Schema(
        fields={
            "name": DummyField(),
            "age": DummyField(default=0),
            "id": DummyField(read_only=True),
        }
    )

    # Missing required 'name'
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"age": 10})
    assert any(msg.code == "required" and msg.index == ["name"] for msg in excinfo.value.messages)

    # Invalid key type
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({123: "value", "name": "Alice"})
    assert any(msg.code == "invalid_key" and msg.index == [123] for msg in excinfo.value.messages)

    # Default applied and read_only ignored
    validated = schema.validate({"name": "Alice"})
    assert validated == {"name": "Alice", "age": 0}
