import pytest
from typesystem.schemas import Definitions
from typesystem.json_schema import if_then_else_from_json_schema, from_json_schema
from typesystem.fields import Any, NeverMatch, Integer, String, Const, IfThenElse

def test_if_then_else_basic():
    """Verify that a simple if/then/else schema produces an IfThenElse field with correct clauses."""
    schema = {
        "if": {"type": "integer"},
        "then": {"type": "string"},
        "else": {"const": 42},
        "default": "fallback"
    }
    definitions = Definitions()
    field = if_then_else_from_json_schema(schema, definitions)

    assert isinstance(field, IfThenElse)
    # The if_clause should be an Integer field
    assert isinstance(field.if_clause, Integer)
    # The then_clause should be a String field
    assert isinstance(field.then_clause, String)
    # The else_clause should be a Const field with value 42
    assert isinstance(field.else_clause, Const)
    assert field.else_clause.const == 42
    # Default value should be propagated
    assert field.default == "fallback"

def test_if_then_else_missing_then_or_else():
    """If 'then' or 'else' are omitted, the corresponding clause should be None."""
    schema = {
        "if": {"type": "boolean"},
        "else": {"type": "integer"},
    }
    definitions = Definitions()
    field = if_then_else_from_json_schema(schema, definitions)

    assert isinstance(field, IfThenElse)
    assert isinstance(field.if_clause, Any)  # boolean maps to Any
    assert field.then_clause is None
    assert isinstance(field.else_clause, Integer)

def test_if_then_else_with_boolean_condition():
    """When the 'if' key is a boolean, the function should return a field that matches the boolean."""
    schema_true = {"if": True}
    schema_false = {"if": False}
    definitions = Definitions()

    field_true = if_then_else_from_json_schema(schema_true, definitions)
    field_false = if_then_else_from_json_schema(schema_false, definitions)

    assert isinstance(field_true, Any)
    assert isinstance(field_false, NeverMatch)
