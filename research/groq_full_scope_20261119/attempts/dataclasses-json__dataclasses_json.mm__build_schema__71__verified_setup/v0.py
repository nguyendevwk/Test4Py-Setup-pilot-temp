import pytest
from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from dataclasses_json.mm import build_schema
from marshmallow.exceptions import ValidationError

# A simple dataclass with various field types
@dataclass
class Sample:
    id: int
    name: str
    value: Optional[Decimal] = None
    tags: List[str] = field(default_factory=list)
    created: datetime = field(default_factory=datetime.utcnow)
    uid: UUID = field(default_factory=UUID)

# Test normal serialization and deserialization
def test_build_schema_normal():
    SchemaCls = build_schema(Sample, mixin=None, infer_missing=False, partial=False)
    schema = SchemaCls()
    obj = Sample(id=1, name="test", value=Decimal("10.5"), tags=["a", "b"])
    dumped = schema.dump(obj)
    # Ensure all fields are present in the dumped dict
    assert set(dumped.keys()) == {"id", "name", "value", "tags", "created", "uid"}
    # Deserialize back to object
    loaded = schema.load(dumped)
    assert isinstance(loaded, Sample)
    assert loaded.id == obj.id
    assert loaded.name == obj.name
    assert loaded.value == obj.value
    assert loaded.tags == obj.tags
    # created and uid are auto-generated, just check types
    assert isinstance(loaded.created, datetime)
    assert isinstance(loaded.uid, UUID)

# Test boundary: optional field omitted and default list handling
def test_build_schema_optional_and_default():
    SchemaCls = build_schema(Sample, mixin=None, infer_missing=False, partial=False)
    schema = SchemaCls()
    # Omit optional field 'value' and list field 'tags'
    data = {"id": 2, "name": "boundary", "created": datetime.utcnow().isoformat(), "uid": UUID(int=0)}
    loaded = schema.load(data)
    assert loaded.value is None
    assert loaded.tags == []
    # Dump back and ensure optional field is omitted if None
    dumped = schema.dump(loaded)
    assert "value" not in dumped or dumped["value"] is None

# Test error: missing required field triggers ValidationError
def test_build_schema_missing_required():
    SchemaCls = build_schema(Sample, mixin=None, infer_missing=False, partial=False)
    schema = SchemaCls()
    # Omit required field 'name'
    data = {"id": 3, "created": datetime.utcnow().isoformat(), "uid": UUID(int=0)}
    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    # Ensure the error message references the missing field
    assert "name" in str(excinfo.value)
