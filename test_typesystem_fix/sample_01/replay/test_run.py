import pytest
from typesystem.schemas import Schema
from typesystem.fields import String, Integer

def test_schema_validate_applies_defaults_and_skips_read_only():
    schema = Schema(
        fields={
            "name": String(default="unknown"),
            "age": Integer(),
            "id": Integer(read_only=True),
        }
    )
    validated = schema.validate({"age": 30, "id": 5})
    assert isinstance(validated, dict)
    assert validated == {"name": "unknown", "age": 30}
    assert "id" not in validated
