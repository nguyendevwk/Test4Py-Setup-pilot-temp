import pytest
from typesystem.schemas import Schema, ValidationError

class DummyField:
    def __init__(self, *, read_only=False, default=None):
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

def test_schema_validate_and_defaults_and_errors():
    a_field = DummyField()
    b_field = DummyField(default=42)
    schema = Schema(fields={"a": a_field, "b": b_field}, allow_null=False)

    # Missing required field 'a'
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({})
    assert any(msg.code == "required" and msg.index == ["a"] for msg in excinfo.value.messages)

    # Valid input with default for missing 'b'
    result = schema.validate({"a": 10})
    assert result == {"a": 10, "b": 42}

    # Non‑string key triggers invalid_key error
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({1: "x", "a": 5})
    assert any(msg.code == "invalid_key" for msg in excinfo.value.messages)

    # allow_null=True accepts None
    schema_null = Schema(fields={"a": a_field}, allow_null=True)
    assert schema_null.validate(None) is None

    # allow_null=False rejects None
    with pytest.raises(ValidationError) as excinfo:
        schema_null.validate(None)
    assert any(msg.code == "null" for msg in excinfo.value.messages)
