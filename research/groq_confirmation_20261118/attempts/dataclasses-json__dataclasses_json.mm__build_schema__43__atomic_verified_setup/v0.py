import pytest
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from dataclasses_json.mm import build_schema
from marshmallow.exceptions import ValidationError

# Helper mixin that does nothing
class DummyMixin:
    pass

# 1. Normal serialization and deserialization
def test_build_schema_basic_serialization(tmp_path):
    @dataclass
    class Person:
        name: str
        age: int
        tags: List[str] = field(default_factory=list)

    PersonSchema = build_schema(Person, DummyMixin, infer_missing=True, partial=False)
    schema = PersonSchema()

    person = Person(name="Alice", age=30, tags=["engineer", "python"])
    json_str = schema.dumps(person)
    # dumps should produce a JSON string
    assert isinstance(json_str, str)
    # Load back to object
    loaded = schema.loads(json_str)
    assert loaded == person

# 2. Partial loading (missing optional fields)
def test_build_schema_partial_loading(tmp_path):
    @dataclass
    class Event:
        title: str
        date: datetime
        location: Optional[str] = None

    EventSchema = build_schema(Event, DummyMixin, infer_missing=True, partial=True)
    schema = EventSchema()

    # Provide only required fields
    data = {"title": "Meeting", "date": "2024-01-01T10:00:00"}
    loaded = schema.load(data)
    assert loaded.title == "Meeting"
    assert loaded.location is None
    # Dump should include all fields
    dumped = schema.dump(loaded)
    assert "location" in dumped
    assert dumped["location"] is None

# 3. Error when required field is missing
def test_build_schema_missing_required(tmp_path):
    @dataclass
    class Product:
        id: UUID
        name: str

    ProductSchema = build_schema(Product, DummyMixin, infer_missing=True, partial=False)
    schema = ProductSchema()

    # Missing 'name' field should raise ValidationError
    data = {"id": "123e4567-e89b-12d3-a456-426614174000"}
    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    assert "name" in str(excinfo.value)
