import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer
from typesystem.base import ValidationError

def test_schema_validate_missing_required_raises_error():
    # A schema with one required field (`name`) and one optional field with a default (`age`).
    schema = Schema(fields={"name": String(), "age": Integer(default=18)})

    # Validate data missing the required `name` key.
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({"age": 20})

    # The ValidationError should contain a Message with code "required" for the missing key.
    messages = excinfo.value.messages()
    assert any(
        m.code == "required" and m.index == ["name"] for m in messages
    ), f"Expected a required error for 'name', got {messages}"
