import pytest
from typesystem.schemas import Schema, ValidationError, Message
from typesystem.fields import String

def test_schema_required_field_missing_raises_validation_error():
    schema = Schema(fields={"name": String()})
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({})
    messages = excinfo.value.messages
    assert len(messages) == 1
    assert messages[0].code == "required"
    assert messages[0].index == ["name"]
