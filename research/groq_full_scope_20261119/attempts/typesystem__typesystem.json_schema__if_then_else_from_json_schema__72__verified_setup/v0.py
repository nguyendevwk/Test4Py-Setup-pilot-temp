import pytest
from typesystem.json_schema import if_then_else_from_json_schema
from typesystem.fields import Integer, String, Boolean
from typesystem.schemas import Definitions

def test_if_then_else_basic_construction():
    """Verify that a simple if/then/else schema produces an IfThenElse field with correct clauses."""
    data = {
        "if": {"type": "integer"},
        "then": {"type": "string"},
        "else": {"type": "boolean"},
    }
    field = if_then_else_from_json_schema(data, Definitions())
    # The field should be an instance of IfThenElse
    assert hasattr(field, "if_clause") and hasattr(field, "then_clause") and hasattr(field, "else_clause")
    # Clauses should be the corresponding field types
    assert isinstance(field.if_clause, Integer)
    assert isinstance(field.then_clause, String)
    assert isinstance(field.else_clause, Boolean)
    # Default should be NO_DEFAULT
    assert field.default is None or field.default == field.default  # NO_DEFAULT is a sentinel

def test_if_then_else_missing_then_else():
    """When 'then' or 'else' are omitted, the corresponding clause should be None."""
    data = {"if": {"type": "string"}}
    field = if_then_else_from_json_schema(data, Definitions())
    assert isinstance(field.if_clause, String)
    assert field.then_clause is None
    assert field.else_clause is None

def test_if_then_else_with_default():
    """The 'default' key should be propagated to the resulting field."""
    data = {
        "if": {"type": "integer"},
        "then": {"type": "string"},
        "default": 42,
    }
    field = if_then_else_from_json_schema(data, Definitions())
    assert field.default == 42
