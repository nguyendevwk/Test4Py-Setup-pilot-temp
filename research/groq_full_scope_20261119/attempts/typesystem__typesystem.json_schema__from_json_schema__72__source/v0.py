import pytest
from typesystem.json_schema import from_json_schema
from typesystem.fields import Any, NeverMatch, Enum, Const, AllOf, Reference
from typesystem.schemas import Definitions

def test_bool_true_and_false():
    # True should map to Any, False to NeverMatch
    assert isinstance(from_json_schema(True), Any)
    assert isinstance(from_json_schema(False), NeverMatch)

def test_enum_and_const():
    # Enum schema should produce an Enum field with correct values
    enum_schema = {"enum": ["red", "green", "blue"]}
    enum_field = from_json_schema(enum_schema)
    assert isinstance(enum_field, Enum)
    assert enum_field.values == ("red", "green", "blue")

    # Const schema should produce a Const field with the correct value
    const_schema = {"const": 42}
    const_field = from_json_schema(const_schema)
    assert isinstance(const_field, Const)
    assert const_field.value == 42

def test_allof_and_ref():
    # Define a component schema and reference it
    definitions = Definitions()
    definitions["#/components/schemas/PositiveInt"] = from_json_schema(
        {"type": "integer", "minimum": 1}
    )
    ref_schema = {"$ref": "#/components/schemas/PositiveInt"}
    ref_field = from_json_schema(ref_schema, definitions=definitions)
    assert isinstance(ref_field, Reference)
    assert ref_field.ref == "#/components/schemas/PositiveInt"

    # allOf schema should combine constraints into an AllOf field
    allof_schema = {
        "allOf": [
            {"type": "integer"},
            {"minimum": 10},
            {"maximum": 20}
        ]
    }
    allof_field = from_json_schema(allof_schema)
    assert isinstance(allof_field, AllOf)
    # The AllOf should contain three constraints: Integer, Minimum, Maximum
    constraint_types = {type(c).__name__ for c in allof_field.constraints}
    assert {"Integer", "Minimum", "Maximum"} <= constraint_types
