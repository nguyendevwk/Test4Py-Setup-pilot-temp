import pytest
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from marshmallow.exceptions import ValidationError

from dataclasses_json.mm import build_schema


# ----------------------------------------------------------------------
# Helper dataclass for testing
# ----------------------------------------------------------------------
@dataclass
class Person:
    name: str
    age: int
    email: str | None = None
    id: UUID = field(default_factory=UUID)


# ----------------------------------------------------------------------
# Test 1: Normal serialization and deserialization
# ----------------------------------------------------------------------
def test_build_schema_normal_serialization():
    # Build a schema for Person
    PersonSchema = build_schema(Person, mixin=None, infer_missing=True, partial=False)

    # Create an instance
    person = Person(name="Alice", age=30, email="alice@example.com", id=UUID("12345678-1234-5678-1234-567812345678"))

    # Serialize to JSON string
    json_str = PersonSchema().dumps(person)
    assert isinstance(json_str, str)
    assert '"name":"Alice"' in json_str
    assert '"age":30' in json_str
    assert '"email":"alice@example.com"' in json_str
    assert '"id":"12345678-1234-5678-1234-567812345678"' in json_str

    # Deserialize back to dataclass
    loaded = PersonSchema().loads(json_str)
    assert isinstance(loaded, Person)
    assert loaded.name == "Alice"
    assert loaded.age == 30
    assert loaded.email == "alice@example.com"
    assert loaded.id == UUID("12345678-1234-5678-1234-567812345678")


# ----------------------------------------------------------------------
# Test 2: Partial loading (missing optional field)
# ----------------------------------------------------------------------
def test_build_schema_partial_loading():
    # Build a schema with partial=True to allow missing fields
    PersonSchema = build_schema(Person, mixin=None, infer_missing=True, partial=True)

    # JSON missing the optional email field
    json_str = '{"name":"Bob","age":25,"id":"12345678-1234-5678-1234-567812345678"}'

    # Should load without error
    loaded = PersonSchema().loads(json_str)
    assert isinstance(loaded, Person)
    assert loaded.name == "Bob"
    assert loaded.age == 25
    assert loaded.email is None
    assert loaded.id == UUID("12345678-1234-5678-1234-567812345678")

    # Dumping should include the missing field as None
    dumped = PersonSchema().dump(loaded)
    assert dumped["email"] is None


# ----------------------------------------------------------------------
# Test 3: Validation error on missing required field
# ----------------------------------------------------------------------
def test_build_schema_missing_required_field():
    # Build a schema with partial=False (default)
    PersonSchema = build_schema(Person, mixin=None, infer_missing=True, partial=False)

    # JSON missing the required 'name' field
    json_str = '{"age":40,"id":"12345678-1234-5678-1234-567812345678"}'

    # Loading should raise ValidationError
    with pytest.raises(ValidationError) as excinfo:
        PersonSchema().loads(json_str)

    # The error message should mention the missing field
    assert "name" in str(excinfo.value)
