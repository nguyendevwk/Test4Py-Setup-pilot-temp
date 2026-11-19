import pytest
from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID
from dataclasses_json.mm import build_schema
from marshmallow import ValidationError

# Helper dataclass for testing
@dataclass
class Person:
    name: str
    age: int
    email: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    uid: UUID = field(default_factory=UUID)

# 1. Test normal serialization and deserialization
def test_person_schema_roundtrip():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=True, partial=False)
    person = Person(name="Alice", age=30, email="alice@example.com", tags=["admin"], uid=UUID("12345678-1234-5678-1234-567812345678"))
    # Serialize
    dumped = PersonSchema().dump(person)
    assert isinstance(dumped, dict)
    assert dumped["name"] == "Alice"
    assert dumped["age"] == 30
    assert dumped["email"] == "alice@example.com"
    assert dumped["tags"] == ["admin"]
    # Deserialize
    loaded = PersonSchema().load(dumped)
    assert isinstance(loaded, Person)
    assert loaded.name == "Alice"
    assert loaded.age == 30
    assert loaded.email == "alice@example.com"
    assert loaded.tags == ["admin"]
    assert loaded.uid == UUID("12345678-1234-5678-1234-567812345678")

# 2. Test optional field handling and allow_none
def test_optional_field_allow_none():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=True, partial=False)
    # Omit optional email
    data_missing_email = {"name": "Bob", "age": 25, "tags": [], "uid": "12345678-1234-5678-1234-567812345678"}
    loaded = PersonSchema().load(data_missing_email)
    assert loaded.email is None
    # Explicitly set email to None
    data_none_email = {"name": "Bob", "age": 25, "email": None, "tags": [], "uid": "12345678-1234-5678-1234-567812345678"}
    loaded_none = PersonSchema().load(data_none_email)
    assert loaded_none.email is None

# 3. Test error when required field missing
def test_missing_required_field_raises():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    # Omit required name field
    data_missing_name = {"age": 40, "tags": [], "uid": "12345678-1234-5678-1234-567812345678"}
    with pytest.raises(ValidationError) as excinfo:
        PersonSchema().load(data_missing_name)
    assert "name" in str(excinfo.value)
