import pytest
from typesystem.composites import IfThenElse
from typesystem.fields import Int, Str, Any

def test_then_clause_success():
    """When the if_clause validates, the then_clause is used."""
    field = IfThenElse(
        if_clause=Int(min=0),
        then_clause=Str(max_length=5),
        else_clause=Str(max_length=3)
    )
    # Value satisfies if_clause (>=0) and then_clause (<=5 chars)
    result = field.validate("hello")
    assert result == "hello"

def test_else_clause_success():
    """When the if_clause fails, the else_clause is used."""
    field = IfThenElse(
        if_clause=Int(min=0),
        then_clause=Str(max_length=5),
        else_clause=Str(max_length=3)
    )
    # Value fails if_clause (negative int) but passes else_clause
    result = field.validate(-1)
    assert result == -1

def test_then_clause_error_propagates():
    """If the then_clause raises a validation error, it propagates."""
    field = IfThenElse(
        if_clause=Int(min=0),
        then_clause=Str(max_length=2),  # too restrictive
        else_clause=Str(max_length=3)
    )
    with pytest.raises(ValueError) as excinfo:
        field.validate("toolong")
    assert "too long" in str(excinfo.value)
