import pytest
from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
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

# 1. Test normal serialization and deserialization
def test_build_schema_normal():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
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

# 2. Test boundary: optional field omitted and default list handling
def test_build_schema_boundary():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    # Omit optional email and provide empty tags list
    person = Person(name="Bob", age=25, uid=UUID("87654321-4321-8765-4321-876543218765"))
    json_data = PersonSchema().dumps(person)
    loaded = PersonSchema().loads(json_data)
    assert loaded.email is None
    assert loaded.tags == []

# 3. Test error: invalid type for a field triggers ValidationError
def test_build_schema_error():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    # Provide a string where an int is expected for age
    bad_json = {
        "name": "Charlie",
        "age": "not_an_int",
        "uid": "12345678-1234-5678-1234-567812345678"
    }
    with pytest.raises(ValidationError) as excinfo:
        PersonSchema().loads(bad_json)
    assert "age" in str(excinfo.value)
