import pytest
from typesystem.schemas import Definitions
from typesystem.json_schema import if_then_else_from_json_schema, from_json_schema
from typesystem.fields import Integer, String, Any, NeverMatch, IfThenElse

def test_if_then_else_normal(tmp_path):
    # Simple schema with if/then/else
    schema = {
        "if": {"type": "integer"},
        "then": {"type": "integer"},
        "else": {"type": "string"},
        "default": 42
    }
    definitions = Definitions()
    field = if_then_else_from_json_schema(schema, definitions)
    assert isinstance(field, IfThenElse)
    # The if_clause should be an Integer field
    assert isinstance(field.if_clause, Integer)
    # then_clause should be Integer, else_clause should be String
    assert isinstance(field.then_clause, Integer)
    assert isinstance(field.else_clause, String)
    # default should be preserved
    assert field.default == 42

def test_if_then_else_missing_then_else(tmp_path):
    # Schema with only if, no then/else
    schema = {"if": {"type": "integer"}}
    definitions = Definitions()
    field = if_then_else_from_json_schema(schema, definitions)
    assert isinstance(field, IfThenElse)
    # then_clause and else_clause should be None
    assert field.then_clause is None
    assert field.else_clause is None
    # if_clause should be Integer
    assert isinstance(field.if_clause, Integer)
    # default should be NO_DEFAULT (None)
    assert field.default is None

def test_if_then_else_invalid_schema(tmp_path):
    # Schema missing required 'if' key
    schema = {"then": {"type": "integer"}}
    definitions = Definitions()
    with pytest.raises(KeyError):
        if_then_else_from_json_schema(schema, definitions)
