import warnings
import pytest
from dataclasses import dataclass, field
from typing import Optional, Union, List
from datetime import datetime
from uuid import UUID
from dataclasses_json.mm import build_type, TYPES
from marshmallow import Schema, fields

# Helper dataclasses for testing
@dataclass
class Inner:
    x: int

@dataclass
class Outer:
    inner: Inner
    maybe: Optional[int]
    union: Union[int, str]
    lst: List[int]

# Dummy mixin to satisfy _issubclass_safe check
class DummyMixin:
    pass

def test_nested_dataclass_field():
    """Test that a nested dataclass field returns a Nested field."""
    # Build field for Outer.inner
    inner_field = build_type(Inner, {}, DummyMixin, field(Inner), Outer)
    assert isinstance(inner_field, fields.Nested)
    # Ensure that the nested schema is correctly set
    assert inner_field.schema.__class__ == Inner.schema().__class__
    # Check that field_many is False for a single nested object
    assert not inner_field.field_many

def test_optional_and_list_fields():
    """Test that optional and list types are handled correctly."""
    # Optional[int] should set allow_none=True
    opt_field = build_type(Optional[int], {}, DummyMixin, field(Optional[int]), Outer)
    assert isinstance(opt_field, fields.Int)
    assert opt_field.allow_none is True

    # List[int] should return a List field with Int as inner
    list_field = build_type(List[int], {}, DummyMixin, field(List[int]), Outer)
    assert isinstance(list_field, fields.List)
    assert isinstance(list_field.inner, fields.Int)

def test_union_field_serialization_and_deserialization():
    """Test that Union fields serialize and deserialize correctly."""
    # Build Union field for Outer.union
    union_field = build_type(Union[int, str], {}, DummyMixin, field(Union[int, str]), Outer)
    assert isinstance(union_field, type(TYPES[typing.Union]))

    # Serialize an int value
    serialized_int = union_field._serialize(42, 'union', Outer())
    assert serialized_int == 42

    # Serialize a str value
    serialized_str = union_field._serialize("hello", 'union', Outer())
    assert serialized_str == "hello"

    # Deserialize an int value
    deserialized_int = union_field._deserialize(99, 'union', {})
    assert deserialized_int == 99

    # Deserialize a str value
    deserialized_str = union_field._deserialize("world", 'union', {})
    assert deserialized_str == "world"
