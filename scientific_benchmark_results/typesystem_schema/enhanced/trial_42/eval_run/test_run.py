import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer

def test_schema_default_values_are_applied():
    # Arrange: a schema with a required field and a field that has a default
    schema = Schema(fields={"name": String(), "age": Integer(default=18)})

    # Act: validate data missing the defaulted field
    result_missing_age = schema.validate({"name": "bob"})

    # Assert: the default value is inserted
    assert result_missing_age == {"name": "bob", "age": 18}

    # Act: validate data providing the field explicitly
    result_with_age = schema.validate({"name": "bob", "age": 25})

    # Assert: the provided value overrides the default
    assert result_with_age == {"name": "bob", "age": 25}
