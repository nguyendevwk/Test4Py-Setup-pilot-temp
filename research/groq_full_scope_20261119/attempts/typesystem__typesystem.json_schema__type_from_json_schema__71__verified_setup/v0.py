import pytest
from typesystem.json_schema import type_from_json_schema
from typesystem.fields import (
    Array,
    Boolean,
    Const,
    NeverMatch,
    Union,
    Integer,
    String,
)
from typesystem.schemas import Definitions


def test_single_type_integer():
    """When the schema specifies a single type, the returned field is that type."""
    schema = {"type": "integer"}
    field = type_from_json_schema(schema, Definitions())
    assert isinstance(field, Integer)
    # Integer fields should accept an int and reject a string
    assert field.validate(42) is None
    with pytest.raises(ValueError):
        field.validate("not an int")


def test_multiple_types_union():
    """When the schema lists multiple types, a Union of the corresponding fields is returned."""
    schema = {"type": ["string", "boolean"]}
    field = type_from_json_schema(schema, Definitions())
    assert isinstance(field, Union)
    # The Union should contain a String and a Boolean field
    types_in_union = {type(f) for f in field.any_of}
    assert String in types_in_union
    assert Boolean in types_in_union
    # Validate that the Union accepts either type
    assert field.validate("hello") is None
    assert field.validate(True) is None
    # And rejects a type not in the union
    with pytest.raises(ValueError):
        field.validate(123)


def test_null_only_schema():
    """When the schema has no type but allows null, a Const(None) field is returned."""
    schema = {"type": None}
    field = type_from_json_schema(schema, Definitions())
    assert isinstance(field, Const)
    assert field.value is None
    # The field should accept None and reject other values
    assert field.validate(None) is None
    with pytest.raises(ValueError):
        field.validate("not null")
