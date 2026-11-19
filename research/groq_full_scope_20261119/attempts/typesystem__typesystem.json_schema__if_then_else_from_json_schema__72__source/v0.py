import pytest
from typesystem.json_schema import if_then_else_from_json_schema
from typesystem.fields import Integer, String, Boolean
from typesystem.composites import IfThenElse
from typesystem.schemas import Definitions

def test_if_then_else_basic():
    # Simple schema with if, then, else
    schema = {
        "if": {"type": "integer"},
        "then": {"type": "string"},
        "else": {"type": "boolean"},
    }
    definitions = Definitions()
    field = if_then_else_from_json_schema(schema, definitions)
    assert isinstance(field, IfThenElse)
    assert isinstance(field.if_clause, Integer)
    assert isinstance(field.then_clause, String)
    assert isinstance(field.else_clause, Boolean)
    assert field.default is None

def test_if_then_else_missing_then_else():
    # Schema with only if clause
    schema = {"if": {"type": "string"}}
    definitions = Definitions()
    field = if_then_else_from_json_schema(schema, definitions)
    assert isinstance(field, IfThenElse)
    assert isinstance(field.if_clause, String)
    assert field.then_clause is None
    assert field.else_clause is None

def test_if_then_else_default_value():
    # Schema with default value
    schema = {
        "if": {"type": "integer"},
        "then": {"type": "string"},
        "else": {"type": "boolean"},
        "default": 42,
    }
    definitions = Definitions()
    field = if_then_else_from_json_schema(schema, definitions)
    assert field.default == 42
