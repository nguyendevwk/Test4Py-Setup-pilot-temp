import pytest
from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
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

# 1. Test normal serialization and deserialization
def test_build_schema_normal():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    schema = PersonSchema()
    person = Person(name="Alice", age=30, email="alice@example.com", tags=["admin"], uid=UUID("12345678-1234-5678-1234-567812345678"))
    # Serialize
    dumped = schema.dump(person)
    assert isinstance(dumped, dict)
    assert dumped["name"] == "Alice"
    assert dumped["age"] == 30
    assert dumped["email"] == "alice@example.com"
    assert dumped["tags"] == ["admin"]
    # Deserialize
    loaded = schema.load(dumped)
    assert isinstance(loaded, Person)
    assert loaded.name == "Alice"
    assert loaded.age == 30
    assert loaded.email == "alice@example.com"
    assert loaded.tags == ["admin"]
    assert loaded.uid == UUID("12345678-1234-5678-1234-567812345678")

# 2. Test boundary: optional field omitted
def test_build_schema_optional_missing():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    schema = PersonSchema()
    # Omit optional email
    data = {"name": "Bob", "age": 25, "tags": [], "uid": "12345678-1234-5678-1234-567812345678"}
    loaded = schema.load(data)
    assert isinstance(loaded, Person)
    assert loaded.email is None
    # Dump back
    dumped = schema.dump(loaded)
    assert "email" not in dumped or dumped["email"] is None

# 3. Test error: missing required field
def test_build_schema_missing_required():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    schema = PersonSchema()
    # Omit required 'name'
    data = {"age": 40, "tags": [], "uid": "12345678-1234-5678-1234-567812345678"}
    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    assert "name" in str(excinfo.value)
