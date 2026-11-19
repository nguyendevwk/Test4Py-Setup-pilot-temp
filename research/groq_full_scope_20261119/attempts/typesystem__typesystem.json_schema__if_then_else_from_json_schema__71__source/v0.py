import pytest
from typesystem.schemas import Definitions
from typesystem.json_schema import if_then_else_from_json_schema
from typesystem.fields import Integer, String, Boolean
from typesystem.composites import IfThenElse


def test_if_then_else_with_all_clauses():
    # Define a simple schema with if, then, else clauses
    data = {
        "if": {"type": "integer"},
        "then": {"type": "string"},
        "else": {"type": "boolean"},
        "default": "fallback",
    }
    definitions = Definitions()
    field = if_then_else_from_json_schema(data, definitions)

    assert isinstance(field, IfThenElse)
    assert isinstance(field.if_clause, Integer)
    assert isinstance(field.then_clause, String)
    assert isinstance(field.else_clause, Boolean)
    assert field.default == "fallback"


def test_if_then_else_missing_then_else():
    # Schema with only if clause; then and else should be None
    data = {"if": {"type": "integer"}}
    definitions = Definitions()
    field = if_then_else_from_json_schema(data, definitions)

    assert isinstance(field, IfThenElse)
    assert isinstance(field.if_clause, Integer)
    assert field.then_clause is None
    assert field.else_clause is None
    assert field.default is None


def test_if_then_else_missing_if_raises():
    # Schema missing the required "if" key should raise KeyError
    data = {"then": {"type": "string"}}
    definitions = Definitions()
    with pytest.raises(KeyError):
        if_then_else_from_json_schema(data, definitions)
