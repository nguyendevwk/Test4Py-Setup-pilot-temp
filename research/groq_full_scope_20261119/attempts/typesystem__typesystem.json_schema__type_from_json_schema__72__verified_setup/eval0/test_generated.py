import pytest
from typesystem.json_schema import type_from_json_schema
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
from typesystem.schemas import Definitions

# Helper to create an empty Definitions instance
def empty_definitions() -> Definitions:
    return Definitions()


def test_single_type_integer_field():
    """When the schema specifies a single type, a corresponding Field is returned."""
    schema = {"type": "integer"}
    field = type_from_json_schema(schema, empty_definitions())
    assert isinstance(field, Integer)
    # The field should not allow null unless explicitly specified
    assert field.allow_null is False


def test_multiple_types_union_and_null():
    """When the schema lists multiple types, a Union of the corresponding Fields is returned."""
    schema = {"type": ["string", "null", "number"]}
    field = type_from_json_schema(schema, empty_definitions())
    assert isinstance(field, Union)
    # The Union should contain exactly two concrete types (string and number) and allow null
    concrete_types = {type(f) for f in field.any_of}
    assert concrete_types == {String, Number}
    assert field.allow_null is True
    # Ensure the Union's any_of list preserves the order of the original types
    assert isinstance(field.any_of[0], String)
    assert isinstance(field.any_of[1], Number)


def test_no_type_with_null_allowed():
    """When no type is specified but null is allowed, a Const(None) is returned."""
    schema = {"type": ["null"]}
    field = type_from_json_schema(schema, empty_definitions())
    assert isinstance(field, Const)
    assert field.value is None
    # The field should allow null
    assert field.allow_null is True
