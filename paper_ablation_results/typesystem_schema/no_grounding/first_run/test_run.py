import pytest
from typesystem.schemas import Schema, ValidationError
from typesystem.fields import String

def test_schema_invalid_key_raises_validation_error():
    # Schema with a required string field
    schema = Schema(fields={"name": String()})
    # Provide a non‑string key along with the required key to avoid a "required" error
    invalid_input = {123: "value", "name": "John"}

    with pytest.raises(ValidationError) as excinfo:
        schema.validate(invalid_input)

    err = excinfo.value
    # There should be exactly one error message: the invalid key
    assert len(err.messages) == 1
    msg = err.messages[0]
    assert msg.code == "invalid_key"
    assert msg.index == [123]
