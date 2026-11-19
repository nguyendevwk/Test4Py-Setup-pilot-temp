import pytest
from typesystem.json_schema import type_from_json_schema, get_valid_types
from typesystem.schemas import Definitions
from typesystem.fields import String, Const, Union, NeverMatch

definitions = Definitions()


def test_single_type_string():
    """When the schema specifies a single type, the returned field is that type."""
    schema = {"type": "string"}
    field = type_from_json_schema(schema, definitions)
    assert isinstance(field, String)
    assert field.allow_null is False


def test_multiple_types_union():
    """When the schema specifies multiple types, a Union of the corresponding fields is returned."""
    schema = {"type": ["string", "number"]}
    field = type_from_json_schema(schema, definitions)
    assert isinstance(field, Union)
    # Union should contain exactly two items: String and Number
    item_types = {type(item).__name__ for item in field.any_of}
    assert item_types == {"String", "Number"}
    assert field.allow_null is False


def test_null_and_string_union_allow_null():
    """When 'null' is one of the types, the Union should allow null."""
    schema = {"type": ["null", "string"]}
    field = type_from_json_schema(schema, definitions)
    assert isinstance(field, Union)
    # Union should contain String and allow_null True
    item_types = {type(item).__name__ for item in field.any_of}
    assert item_types == {"String"}
    assert field.allow_null is True


def test_no_type_returns_const_or_nevermatch():
    """When no type is specified, the function returns Const(None) if allow_null is True,
    otherwise NeverMatch."""
    # No type specified, but allow_null is True via explicit null type
    schema = {"type": ["null"]}
    field = type_from_json_schema(schema, definitions)
    assert isinstance(field, Const)
    assert field.value is None

    # No type specified and no null, should return NeverMatch
    schema = {}
    field = type_from_json_schema(schema, definitions)
    assert isinstance(field, NeverMatch)
