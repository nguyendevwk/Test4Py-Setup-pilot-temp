import pytest
from dataclasses import dataclass, field
from typing import Optional, Union, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from dataclasses_json import mm
from dataclasses_json.mm import schema, build_type, _UnionField, _TupleVarLen, _TimestampField
from marshmallow import Schema, ValidationError

# Helper dataclasses for testing
@dataclass
class Simple:
    a: int
    b: str = "default"
    c: Optional[float] = None
    d: UUID = field(default_factory=UUID)

@dataclass
class UnionExample:
    x: Union[int, str]
    y: Union[List[int], List[str]]

# Test 1: Basic schema generation and serialization/deserialization
def test_simple_schema_roundtrip():
    simple_schema = Schema.from_dict(schema(Simple, mm, infer_missing=True))
    obj = Simple(a=10, b="hello", c=3.14, d=UUID("12345678-1234-5678-1234-567812345678"))
    dumped = simple_schema.dump(obj)
    assert dumped == {
        "a": 10,
        "b": "hello",
        "c": 3.14,
        "d": "12345678-1234-5678-1234-567812345678",
    }
    loaded = simple_schema.load(dumped)
    assert loaded == obj

# Test 2: Optional and required field handling
def test_optional_and_required_behavior():
    simple_schema = Schema.from_dict(schema(Simple, mm, infer_missing=False))
    # 'b' has default, 'c' is optional, 'a' is required
    data = {"a": 5}
    loaded = simple_schema.load(data)
    assert loaded.b == "default"
    assert loaded.c is None
    # Missing required field should raise ValidationError
    with pytest.raises(ValidationError):
        simple_schema.load({"b": "missing"})

# Test 3: Union field serialization with type hinting
def test_union_field_serialization():
    union_schema = Schema.from_dict(schema(UnionExample, mm, infer_missing=True))
    obj_int = UnionExample(x=42, y=[1, 2, 3])
    dumped_int = union_schema.dump(obj_int)
    assert dumped_int["x"] == 42
    assert dumped_int["y"] == [1, 2, 3]
    loaded_int = union_schema.load(dumped_int)
    assert loaded_int == obj_int

    obj_str = UnionExample(x="hello", y=["a", "b"])
    dumped_str = union_schema.dump(obj_str)
    assert dumped_str["x"] == "hello"
    assert dumped_str["y"] == ["a", "b"]
    loaded_str = union_schema.load(dumped_str)
    assert loaded_str == obj_str
