import pytest
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from dataclasses_json.mm import build_schema
from marshmallow.exceptions import ValidationError

# A simple dataclass with various field types
@dataclass
class Sample:
    id: int
    name: str
    optional: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created: datetime = field(default_factory=datetime.utcnow)
    uid: UUID = field(default_factory=UUID)

# 1. Test normal serialization and deserialization
def test_build_schema_normal(tmp_path):
    # Build the schema
    SampleSchema = build_schema(Sample, mixin=None, infer_missing=False, partial=False)

    # Create an instance
    obj = Sample(id=1, name="test", optional="opt", tags=["a", "b"], uid=UUID(int=1))
    # Serialize to JSON string
    json_str = SampleSchema().dumps(obj)
    # Deserialize back to object
    loaded = SampleSchema().loads(json_str)
    assert isinstance(loaded, Sample)
    assert loaded.id == obj.id
    assert loaded.name == obj.name
    assert loaded.optional == obj.optional
    assert loaded.tags == obj.tags
    assert loaded.uid == obj.uid

# 2. Test boundary: missing optional field and partial loading
def test_build_schema_partial_and_missing(tmp_path):
    SampleSchema = build_schema(Sample, mixin=None, infer_missing=False, partial=True)
    # Create JSON missing the optional field
    data = {"id": 2, "name": "partial", "tags": [], "uid": str(UUID(int=2))}
    # Load with partial=True should succeed
    loaded = SampleSchema().loads(data)
    assert isinstance(loaded, Sample)
    assert loaded.optional is None
    # Dump should include all fields, including optional as None
    dumped = SampleSchema().dump(loaded)
    assert dumped["optional"] is None

# 3. Test error: invalid type for a field
def test_build_schema_invalid_type():
    SampleSchema = build_schema(Sample, mixin=None, infer_missing=False, partial=False)
    # Provide wrong type for 'id' (string instead of int)
    data = {"id": "not_an_int", "name": "error", "tags": [], "uid": str(UUID(int=3))}
    with pytest.raises(ValidationError) as excinfo:
        SampleSchema().loads(data)
    assert "id" in str(excinfo.value)
