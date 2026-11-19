import pytest
from typesystem.schemas import Schema, Field

class DummyField(Field):
    def __init__(self, *, read_only=False, default=None):
        super().__init__(read_only=read_only)
        self._default = default

    def has_default(self):
        return self._default is not None

    def get_default_value(self):
        return self._default

    def validate_or_error(self, value):
        return value, None

    def serialize(self, value):
        return value

def test_schema_validate_applies_defaults_and_excludes_read_only():
    fields = {
        'a': DummyField(),
        'b': DummyField(default=42),
        'c': DummyField(read_only=True),
    }
    schema = Schema(fields, allow_null=False)
    input_value = {'a': 1}
    result = schema.validate(input_value)
    assert result == {'a': 1, 'b': 42}
    assert 'c' not in result
