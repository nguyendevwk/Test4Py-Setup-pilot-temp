import typing
import pytest
from typesystem.schemas import Schema, Field
from typesystem.exceptions import ValidationError, Message


class DummyField(Field):
    def __init__(self, *, read_only: bool = False, default: typing.Any = None, allow_null: bool = False):
        super().__init__(allow_null=allow_null)
        self.read_only = read_only
        self.default = default

    def has_default(self) -> bool:
        return self.default is not None

    def get_default_value(self) -> typing.Any:
        return self.default

    def validate_or_error(self, value: typing.Any) -> tuple[typing.Any, typing.Optional[ValidationError]]:
        # Accept any value; no error
        return value, None

    def serialize(self, value: typing.Any) -> typing.Any:
        return value


def test_schema_validation_and_defaults():
    fields = {
        "a": DummyField(),
        "b": DummyField(default=5),
        "c": DummyField(read_only=True),
    }
    schema = Schema(fields=fields)

    # Valid input: required 'a' present, default 'b' applied, read-only 'c' ignored
    validated = schema.validate({"a": 1})
    assert validated == {"a": 1, "b": 5}

    # Missing required 'a' triggers ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({})
    assert any(msg.code == "required" and msg.index == ["a"] for msg in excinfo.value.messages)

    # Invalid key type triggers ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"a": 1, 2: 3})
    assert any(msg.code == "invalid_key" and msg.index == [2] for msg in excinfo.value.messages)

    # Null value not allowed triggers ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(None)
    assert any(msg.code == "null" for msg in excinfo.value.messages)

    # Non-dict type triggers ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema.validate(42)
    assert any(msg.code == "type" for msg in excinfo.value.messages)

    # Schema with allow_null returns None for None input
    schema_null = Schema(fields=fields, allow_null=True)
    assert schema_null.validate(None) is None

    # Serialization omits read-only fields and uses field.serialize
    obj = {"a": 1, "b": 5, "c": 10}
    serialized = schema.serialize(obj)
    assert serialized == {"a": 1, "b": 5}
