import pytest
from typesystem.schemas import Schema, Field, ValidationError


class DummyField(Field):
    def __init__(self, *, default=None, read_only=False):
        super().__init__()
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


def test_schema_validate_required_and_defaults():
    schema = Schema(
        fields={
            "required": DummyField(),
            "optional": DummyField(default=10),
            "read_only": DummyField(read_only=True, default=5),
        }
    )

    # Missing required field should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"optional": 20})
    assert any(
        msg.code == "required" and msg.index == ["required"]
        for msg in excinfo.value.messages
    )

    # Valid input with required only; optional gets default
    result = schema.validate({"required": 1})
    assert result == {"required": 1, "optional": 10}

    # Valid input with required and optional provided
    result = schema.validate({"required": 2, "optional": 3})
    assert result == {"required": 2, "optional": 3}

    # Read-only field present in input should be ignored
    result = schema.validate({"required": 4, "read_only": 99})
    assert result == {"required": 4, "optional": 10}
