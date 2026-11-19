import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_schema_required_and_default_behavior():
    # Field 'name' has no default → required; 'age' has default → optional
    schema = Schema(fields={"name": String(), "age": Integer(default=18)})

    # Missing required key should raise ValidationError with code 'required'
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"age": 25})
    messages = excinfo.value.messages
    assert any(m.code == "required" and m.index == ["name"] for m in messages)

    # Missing optional key should use default value
    result = schema.validate({"name": "bob"})
    assert result == {"name": "bob", "age": 18}

    # All required keys present should succeed
    result = schema.validate({"name": "alice", "age": 30})
    assert result == {"name": "alice", "age": 30}
