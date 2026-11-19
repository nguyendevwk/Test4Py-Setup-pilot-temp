import pytest
from typesystem.schemas import Definitions
from typesystem.composites import IfThenElse
from typesystem.json_schema import if_then_else_from_json_schema

def test_if_then_else_normal(tmp_path):
    # Create minimal definitions (empty)
    defs = Definitions()
    # Define a simple JSON schema with if, then, else and default
    schema = {
        "if": {"type": "string"},
        "then": {"type": "integer"},
        "else": {"type": "boolean"},
        "default": "fallback",
    }
    field = if_then_else_from_json_schema(schema, definitions=defs)
    assert isinstance(field, IfThenElse)
    # The field should expose the clauses as attributes
    assert hasattr(field, "if_clause")
    assert hasattr(field, "then_clause")
    assert hasattr(field, "else_clause")
    assert field.default == "fallback"

def test_if_then_else_missing_then_else(tmp_path):
    defs = Definitions()
    schema = {"if": {"type": "number"}}
    field = if_then_else_from_json_schema(schema, definitions=defs)
    assert isinstance(field, IfThenElse)
    # then_clause and else_clause should be None when omitted
    assert field.then_clause is None
    assert field.else_clause is None
    # default should be NO_DEFAULT (imported from typesystem.fields)
    from typesystem.fields import NO_DEFAULT
    assert field.default == NO_DEFAULT

def test_if_then_else_missing_if(tmp_path):
    defs = Definitions()
    schema = {"then": {"type": "string"}}
    with pytest.raises(KeyError):
        if_then_else_from_json_schema(schema, definitions=defs)
