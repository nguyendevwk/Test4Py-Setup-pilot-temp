import pytest
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from dataclasses_json.mm import build_schema
from marshmallow.exceptions import ValidationError

# Helper dataclass for testing
@dataclass
class Person:
    name: str
    age: int
    email: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    uid: UUID = field(default_factory=UUID)

# Test normal serialization and deserialization
def test_build_schema_normal(tmp_path):
    # Build schema with default settings
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    schema = PersonSchema()
    # Create instance
    person = Person(name="Alice", age=30, email="alice@example.com", tags=["admin"], uid=UUID("12345678-1234-5678-1234-567812345678"))
    # Dump to dict
    dumped = schema.dump(person)
    assert isinstance(dumped, dict)
    assert dumped["name"] == "Alice"
    assert dumped["age"] == 30
    assert dumped["email"] == "alice@example.com"
    assert dumped["tags"] == ["admin"]
    # Load back to dataclass
    loaded = schema.load(dumped)
    assert isinstance(loaded, Person)
    assert loaded == person

# Test boundary: optional field omitted and many=True
def test_build_schema_optional_and_many(tmp_path):
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    schema = PersonSchema(many=True)
    # Create list of persons, one without email
    persons = [
        Person(name="Bob", age=25, tags=["user"], uid=UUID("87654321-4321-8765-4321-876543218765")),
        Person(name="Carol", age=28, tags=[], uid=UUID("11223344-5566-7788-99aa-bbccddeeff00"))
    ]
    # Dump list
    dumped_list = schema.dump(persons)
    assert isinstance(dumped_list, list)
    assert len(dumped_list) == 2
    # Email should be omitted for second person
    assert "email" not in dumped_list[1]
    # Load back
    loaded_list = schema.load(dumped_list)
    assert isinstance(loaded_list, list)
    assert loaded_list[0].email == "bob@example.com"  # default None
    assert loaded_list[1].email is None

# Test error handling: missing required field
def test_build_schema_missing_required():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    schema = PersonSchema()
    # Missing required 'name' field
    bad_data = {"age": 40, "email": "bob@example.com", "tags": [], "uid": "12345678-1234-5678-1234-567812345678"}
    with pytest.raises(ValidationError) as excinfo:
        schema.load(bad_data)
    assert "name" in str(excinfo.value)
