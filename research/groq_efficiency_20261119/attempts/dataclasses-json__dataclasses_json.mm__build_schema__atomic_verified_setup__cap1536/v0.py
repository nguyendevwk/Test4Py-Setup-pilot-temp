import pytest
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from dataclasses_json.mm import build_schema
from marshmallow.exceptions import ValidationError

# A simple dataclass with various field types
@dataclass
class Person:
    name: str
    age: int
    email: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    uid: UUID = field(default_factory=UUID)

# Helper mixin that does nothing special
class DummyMixin:
    pass

# Test 1: Normal serialization and deserialization
def test_build_schema_normal():
    PersonSchema = build_schema(Person, DummyMixin, infer_missing=True, partial=False)
    person = Person(name="Alice", age=30, email="alice@example.com", tags=["admin"], uid=UUID("12345678-1234-5678-1234-567812345678"))
    # Serialize
    json_data = PersonSchema().dumps(person)
    # Deserialize
    loaded = PersonSchema().loads(json_data)
    assert isinstance(loaded, Person)
    assert loaded.name == "Alice"
    assert loaded.age == 30
    assert loaded.email == "alice@example.com"
    assert loaded.tags == ["admin"]
    assert loaded.uid == UUID("12345678-1234-5678-1234-567812345678")

# Test 2: Boundary case – optional field omitted
def test_build_schema_optional_missing():
    PersonSchema = build_schema(Person, DummyMixin, infer_missing=True, partial=False)
    person = Person(name="Bob", age=25, tags=["user"], uid=UUID("87654321-4321-8765-4321-876543218765"))
    # Serialize without email
    json_data = PersonSchema().dumps(person)
    # Deserialize
    loaded = PersonSchema().loads(json_data)
    assert loaded.email is None
    assert loaded.name == "Bob"
    assert loaded.age == 25
    assert loaded.tags == ["user"]

# Test 3: Error case – invalid type for a field
def test_build_schema_invalid_type():
    PersonSchema = build_schema(Person, DummyMixin, infer_missing=True, partial=False)
    # Prepare JSON with wrong type for age (string instead of int)
    bad_json = {
        "name": "Charlie",
        "age": "not-an-int",
        "tags": ["guest"],
        "uid": "12345678-1234-5678-1234-567812345678"
    }
    with pytest.raises(ValidationError) as excinfo:
        PersonSchema().loads(bad_json)
    assert "age" in str(excinfo.value)
