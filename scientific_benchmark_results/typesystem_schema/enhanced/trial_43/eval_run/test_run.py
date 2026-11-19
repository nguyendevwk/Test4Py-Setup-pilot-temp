import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer

def test_schema_validate_applies_defaults_and_skips_read_only():
    # Schema with a required field, a defaulted field, and a read-only field
    schema = Schema(
        fields={
            "name": String(),          # required (no default, not read-only)
            "age": Integer(default=18),# default value
            "id": Integer(read_only=True),  # read-only, should be ignored
        }
    )

    # Validate input missing the defaulted and read-only fields
    result = schema.validate({"name": "bob"})
    assert result == {"name": "bob", "age": 18}
    assert "id" not in result

    # Validate input providing a value for the read-only field; it should still be ignored
    result_with_id = schema.validate({"name": "bob", "id": 42})
    assert result_with_id == {"name": "bob", "age": 18}
    assert "id" not in result_with_id
