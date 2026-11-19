import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer

def test_schema_applies_default_value_when_key_missing():
    # Arrange: a schema with a defaulted field and a required field
    schema = Schema(fields={"name": String(default="anon"), "age": Integer()})

    # Act: validate input missing the defaulted field
    result = schema.validate({"age": 30})

    # Assert: the default value is inserted and the required field is validated
    assert result == {"name": "anon", "age": 30}
