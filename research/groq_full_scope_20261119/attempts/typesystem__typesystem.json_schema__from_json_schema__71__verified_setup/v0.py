import pytest
from typesystem.json_schema import from_json_schema
from typesystem.fields import Any, NeverMatch, Enum, Array, String, Integer, AllOf


def test_from_json_schema_boolean_true_and_false():
    # Boolean True should map to Any()
    assert from_json_schema(True) is Any()
    # Boolean False should map to NeverMatch()
    assert isinstance(from_json_schema(False), NeverMatch)


def test_from_json_schema_enum_and_type_constraints():
    # Define a JSON schema with an enum and a type constraint
    schema = {
        "type": "string",
        "enum": ["red", "green", "blue"]
    }
    field = from_json_schema(schema)
    # The resulting field should be an Enum of String
    assert isinstance(field, Enum)
    assert isinstance(field.base, String)
    assert field.values == ("red", "green", "blue")


def test_from_json_schema_all_of_composition():
    # Define a schema that uses allOf to combine constraints
    schema = {
        "allOf": [
            {"type": "integer", "minimum": 0},
            {"type": "integer", "maximum": 10}
        ]
    }
    field = from_json_schema(schema)
    # The resulting field should be an AllOf containing two Integer constraints
    assert isinstance(field, AllOf)
    assert len(field.constraints) == 2
    for constraint in field.constraints:
        assert isinstance(constraint, Integer)
    # Ensure the constraints are correctly applied
    assert field.constraints[0].minimum == 0
    assert field.constraints[1].maximum == 10
