import pytest
from typesystem.json_schema import type_from_json_schema, definitions
from typesystem.fields import (
    Any,
    Array,
    Boolean,
    Const,
    Decimal,
    Float,
    Integer,
    Number,
    Object,
    String,
    Union,
)

def test_single_type_integer():
    schema = {"type": "integer"}
    field = type_from_json_schema(schema, definitions)
    assert isinstance(field, Integer)
    assert field.allow_null is False

def test_multiple_types_union():
    schema = {"type": ["string", "null", "boolean"]}
    field = type_from_json_schema(schema, definitions)
    assert isinstance(field, Union)
    assert field.allow_null is True
    # Union should contain String and Boolean fields
    types_in_union = {type(f) for f in field.any_of}
    assert String in types_in_union
    assert Boolean in types_in_union
    # No other types should be present
    assert len(field.any_of) == 2

def test_no_type_with_null_allowed():
    schema = {"format": "date-time"}  # no explicit type
    field = type_from_json_schema(schema, definitions)
    # No type specified defaults to null allowed
    assert isinstance(field, Const)
    assert field.value is None
    assert isinstance(field, Const)
