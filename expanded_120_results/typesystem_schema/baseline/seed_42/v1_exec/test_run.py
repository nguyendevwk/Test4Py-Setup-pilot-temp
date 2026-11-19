import pytest
from typesystem.schemas import Schema, ValidationError, Message, Field

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
        return item, None

    def serialize(self, value):
        return value

def test_schema_validate_applies_defaults_and_ignores_read_only():
    schema = Schema(fields={
        'a': DummyField(),
        'b': DummyField(default=10),
        'c': DummyField(read_only=True)
    })
    # All fields present: read-only field is ignored
    result = schema.validate({'a': 1, 'b': 2, 'c': 3})
    assert result == {'a': 1, 'b': 2}

    # Missing required field 'a' triggers ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({'b': 2, 'c': 3})
    messages = excinfo.value.messages
    assert any(msg.code == 'required' and msg.index == ['a'] for msg in messages)

    # Missing optional field 'b' uses default value
    result = schema.validate({'a': 5, 'c': 3})
    assert result == {'a': 5, 'b': 10}
