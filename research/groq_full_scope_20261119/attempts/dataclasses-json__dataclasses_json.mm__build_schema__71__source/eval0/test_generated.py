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
def test_build_schema_normal_behavior():
    SchemaCls = build_schema(Sample, mixin=None, infer_missing=False, partial=False)
    schema = SchemaCls()
    obj = Sample(id=1, name="test", value=Decimal("10.5"), tags=["a", "b"])
    dumped = schema.dump(obj)
    # Ensure all fields are present in the dumped dict
    assert set(dumped.keys()) == {"id", "name", "value", "tags", "created", "uid"}
    # Ensure types are JSON serializable
    assert isinstance(dumped["id"], int)
    assert isinstance(dumped["name"], str)
    assert isinstance(dumped["value"], str)  # Decimal is serialized as string
    assert isinstance(dumped["tags"], list)
    assert isinstance(dumped["created"], str)  # datetime serialized as ISO string
    assert isinstance(dumped["uid"], str)  # UUID serialized as string

    # Deserialize back to object
    loaded = schema.load(dumped)
    assert isinstance(loaded, Sample)
    assert loaded.id == obj.id
    assert loaded.name == obj.name
    assert loaded.value == obj.value
    assert loaded.tags == obj.tags
    # created and uid are parsed back to appropriate types
    assert isinstance(loaded.created, datetime)
    assert isinstance(loaded.uid, UUID)

# Test boundary: optional field omitted during serialization
def test_build_schema_optional_field_missing():
    SchemaCls = build_schema(Sample, mixin=None, infer_missing=False, partial=False)
    schema = SchemaCls()
    obj = Sample(id=2, name="no value")
    dumped = schema.dump(obj)
    # Optional field should be omitted if None
    assert "value" not in dumped
    # Deserialize should set value to None
    loaded = schema.load(dumped)
    assert loaded.value is None

# Test error: missing required field during deserialization
def test_build_schema_missing_required_field_error():
    SchemaCls = build_schema(Sample, mixin=None, infer_missing=False, partial=False)
    schema = SchemaCls()
    # Remove a required field 'name'
    bad_data = {"id": 3, "value": "5.0", "tags": [], "created": datetime.utcnow().isoformat(), "uid": UUID(int=0).hex}
    with pytest.raises(ValidationError) as excinfo:
        schema.load(bad_data)
    # The error message should mention the missing field
    assert "name" in str(excinfo.value)
