import pytest
from typesystem.json_schema import from_json_schema
from typesystem.fields import Any, NeverMatch, Enum, Array, Integer

def test_boolean_input_returns_correct_field():
    # True should map to Any
    assert isinstance(from_json_schema(True), Any)
    # False should map to NeverMatch
    assert isinstance(from_json_schema(False), NeverMatch)

def test_enum_constraint_parses_correctly():
    schema = {"enum": [1, 2, 3]}
    field = from_json_schema(schema)
    # The resulting field should be an Enum with the given values
    assert hasattr(field, "choices")
    assert set(field.choices) == {1, 2, 3}

def test_all_of_composition_returns_allof_with_constraints():
    schema = {
        "allOf": [
            {"type": "integer"},
            {"minimum": 10},
            {"maximum": 20}
        ]
    }
    field = from_json_schema(schema)
    # The field should be an AllOf instance containing three constraints
    from typesystem.composites import AllOf
    assert isinstance(field, AllOf)
    # Each constraint should be a Field subclass (Integer, Minimum, Maximum)
    constraint_types = {type(c) for c in field.constraints}
    # Integer constraint
    assert any(isinstance(c, Integer) for c in field.constraints)
    # Minimum and Maximum constraints are represented by Integer with bounds
    assert any(hasattr(c, "minimum") for c in field.constraints)
    assert any(hasattr(c, "maximum") for c in field.constraints)
