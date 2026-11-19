import pytest
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from dataclasses_json.mm import build_schema
from marshmallow.exceptions import ValidationError

# ---------------------------------------------------------------------------

@dataclass
class Person:
    name: str
    age: int
    email: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    uid: UUID = field(default_factory=UUID)

# ---------------------------------------------------------------------------

def test_schema_dump_and_load(tmp_path):
    """Normal scenario: dump a dataclass instance and load it back."""
    schema_cls = build_schema(Person, mixin=None, infer_missing=True, partial=False)
    schema = schema_cls()
    person = Person(name="Alice", age=30, email="alice@example.com", tags=["dev", "python"])
    dumped = schema.dump(person)
    # The dumped dict should contain all fields except the catch‑all placeholder
    assert set(dumped.keys()) == {"name", "age", "email", "tags", "uid"}
    # Load back and compare
    loaded = schema.load(dumped)
    assert isinstance(loaded, Person)
    assert loaded.name == person.name
    assert loaded.age == person.age
    assert loaded.email == person.email
    assert loaded.tags == person.tags
    # uid is a UUID, ensure it matches
    assert loaded.uid == person.uid

def test_missing_required_field_raises(tmp_path):
    """Boundary scenario: missing required field should raise ValidationError."""
    schema_cls = build_schema(Person, mixin=None, infer_missing=False, partial=False)
    schema = schema_cls()
    # Omit the required 'age' field
    bad_data = {"name": "Bob", "email": "bob@example.com", "tags": [], "uid": UUID(int=0)}
    with pytest.raises(ValidationError) as excinfo:
        schema.load(bad_data)
    # The error message should mention the missing field
    assert "age" in str(excinfo.value)

def test_partial_load_allows_missing_fields(tmp_path):
    """Error scenario: partial=True allows missing fields during load."""
    schema_cls = build_schema(Person, mixin=None, infer_missing=True, partial=True)
    schema = schema_cls()
    # Provide only the required 'name' field
    partial_data = {"name": "Charlie"}
    loaded = schema.load(partial_data)
    assert isinstance(loaded, Person)
    assert loaded.name == "Charlie"
    # Optional fields should be set to their defaults
    assert loaded.email is None
    assert loaded.tags == []
    # uid should be a UUID instance (default factory)
    assert isinstance(loaded.uid, UUID)
