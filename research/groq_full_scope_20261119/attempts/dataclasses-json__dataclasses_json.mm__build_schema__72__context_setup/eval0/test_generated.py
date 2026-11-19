import pytest
from dataclasses import dataclass, field
from typing import Optional, List
from dataclasses_json.mm import build_schema
from marshmallow.exceptions import ValidationError

# Helper dataclass for testing
@dataclass
class Person:
    name: str
    age: int
    nickname: Optional[str] = None
    tags: List[str] = field(default_factory=list)

# Test 1: Normal serialization and deserialization
def test_person_schema_roundtrip():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=True, partial=False)
    schema = PersonSchema()
    data = {"name": "Alice", "age": 30, "nickname": "Al", "tags": ["friend", "colleague"]}
    # Dump to JSON-compatible dict
    dumped = schema.dump(data)
    assert dumped == {"name": "Alice", "age": 30, "nickname": "Al", "tags": ["friend", "colleague"]}
    # Load back to dataclass instance
    loaded = schema.load(dumped)
    assert isinstance(loaded, Person)
    assert loaded.name == "Alice"
    assert loaded.age == 30
    assert loaded.nickname == "Al"
    assert loaded.tags == ["friend", "colleague"]

# Test 2: Optional field omitted and default handling
def test_optional_field_missing():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=True, partial=False)
    schema = PersonSchema()
    # nickname omitted, tags omitted (default_factory)
    data = {"name": "Bob", "age": 25}
    dumped = schema.dump(data)
    assert dumped == {"name": "Bob", "age": 25, "nickname": None, "tags": []}
    loaded = schema.load(dumped)
    assert loaded.nickname is None
    assert loaded.tags == []

# Test 3: Validation error for missing required field
def test_missing_required_field_raises():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    schema = PersonSchema()
    # age omitted, infer_missing=False so required
    data = {"name": "Charlie"}
    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    # Ensure the error message references the missing field
    assert "age" in str(excinfo.value)
