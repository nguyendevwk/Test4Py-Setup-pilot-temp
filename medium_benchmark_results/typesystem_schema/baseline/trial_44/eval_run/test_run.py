import pytest
from typesystem.schemas import Schema, ValidationError
from typesystem.fields import String


def test_schema_invalid_key_detects_non_string_keys():
    # Arrange: schema with a single required field
    schema = Schema(fields={"name": String()})

    # Act & Assert: passing a dict with a non‑string key raises ValidationError
    with pytest.raises(ValidationError) as excinfo:
        schema.validate({123: "value", "name": "Bob"})

    error = excinfo.value
    assert isinstance(error, ValidationError)
    assert len(error.messages) == 1

    msg = error.messages[0]
    assert msg.code == "invalid_key"
    assert msg.index == [123]
    assert msg.text == "All object keys must be strings."
