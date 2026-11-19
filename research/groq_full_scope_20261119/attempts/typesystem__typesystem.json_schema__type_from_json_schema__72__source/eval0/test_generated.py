import pytest
from typesystem.json_schema import type_from_json_schema
from typesystem.fields import Integer, Const, NeverMatch, Union
from typesystem.schemas import Definitions

def test_single_type_integer():
    """When the schema specifies a single type, the returned field is the corresponding field."""
    schema = {"type": "integer"}
    field = type_from_json_schema(schema, Definitions())
    assert isinstance(field, Integer)
    # The field should not allow null unless explicitly specified
    assert not field.allow_null

def test_multiple_types_union():
    """When multiple types are specified, a Union of the corresponding fields is returned."""
    schema = {"type": ["integer", "string"]}
    field = type_from_json_schema(schema, Definitions())
    assert isinstance(field, Union)
    # The Union should contain exactly two items: Integer and String
    types = {type(item).__name__ for item in field.any_of}
    assert types == {"Integer", "String"}
    # Null should not be allowed unless explicitly specified
    assert not field.allow_null

def test_no_type_with_null_and_without_null():
    """When no type is specified, the function returns Const(None) if allow_null is True,
    otherwise NeverMatch."""
    # allow_null True
    schema_null = {"type": None}
    field_null = type_from_json_schema(schema_null, Definitions())
    assert isinstance(field_null, Const)
    assert field_null.value is None

    # allow_null False
    schema_no_null = {}
    field_none = type_from_json_schema(schema_no_null, Definitions())
    assert isinstance(field_none, NeverMatch)
