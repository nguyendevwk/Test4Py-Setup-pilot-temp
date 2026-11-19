import pytest
from typesystem.schemas import Schema, Field
from typesystem.exceptions import ValidationError, Message


class DummyField(Field):
    def __init__(self, *, read_only=False, default=None, allow_null=False, **kwargs):
        super().__init__(read_only=read_only, allow_null=allow_null, **kwargs)
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

    def get_error_text(self, key):
        return f"Error {key}"


def test_schema_validate_required_and_defaults_and_invalid_keys():
    schema = Schema(
        fields={
            "a": DummyField(default=10),
            "b": DummyField(),
            "c": DummyField(read_only=True),
        },
        allow_null=True,
    )

    # allow_null: None should be accepted
    assert schema.validate(None) is None

    # Valid input with all required fields
    assert schema.validate({"a": 5, "b": 20}) == {"a": 5, "b": 20}

    # Missing optional field 'a' should use default
    assert schema.validate({"b": 20}) == {"a": 10, "b": 20}

    # Missing required field 'b' should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"a": 5})
    msgs = excinfo.value.messages
    assert any(m.code == "required" and m.index == ["b"] for m in msgs)

    # Invalid key type should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"a": 5, "b": 20, 42: "x"})
    msgs = excinfo.value.messages
    assert any(m.code == "invalid_key" and m.index == [42] for m in msgs)
