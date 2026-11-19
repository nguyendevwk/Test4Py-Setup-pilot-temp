import json
import pytest
from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID
from dataclasses_json.mm import build_schema
from marshmallow import ValidationError

# Helper dataclass used in tests
@dataclass
class Person:
    name: str
    age: int
    tags: List[str] = field(default_factory=list)
    dataclass_json_config: Optional[str] = None  # should be excluded from schema fields

# Test 1: Normal serialization and deserialization
def test_build_schema_basic_serialization(tmp_path):
    # Build schema for Person
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    schema = PersonSchema()

    # Create an instance
    person = Person(name="Alice", age=30, tags=["engineer", "python"])

    # Dump to JSON string
    json_str = schema.dumps(person)
    data = json.loads(json_str)

    # Verify that all fields except dataclass_json_config are present
    assert set(data.keys()) == {"name", "age", "tags"}
    assert data["name"] == "Alice"
    assert data["age"] == 30
    assert data["tags"] == ["engineer", "python"]

    # Load back to object
    loaded = schema.loads(json_str)
    assert isinstance(loaded, Person)
    assert loaded.name == "Alice"
    assert loaded.age == 30
    assert loaded.tags == ["engineer", "python"]
    # dataclass_json_config should be None by default
    assert loaded.dataclass_json_config is None

# Test 2: Schema Meta fields exclude dataclass_json_config and catch‑all placeholder
def test_build_schema_meta_excludes_special_fields():
    PersonSchema = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    meta_fields = PersonSchema.Meta.fields
    # dataclass_json_config should not be in the fields tuple
    assert "dataclass_json_config" not in meta_fields
    # All other dataclass fields should be present
    expected = ("name", "age", "tags")
    assert meta_fields == expected

# Test 3: Passing a non‑dataclass raises an error
def test_build_schema_non_dataclass_raises():
    class NotADataclass:
        pass

    with pytest.raises(TypeError):
        build_schema(NotADataclass, mixin=None, infer_missing=False, partial=False)
