import pytest
from typesystem.composites import IfThenElse
from typesystem.fields import Any, Int, String, Bool

def test_if_then_else_then_branch():
    """When the if_clause validates, the then_clause is used."""
    field = IfThenElse(if_clause=Int(), then_clause=String(), else_clause=Bool())
    # Value that satisfies Int (e.g., 42)
    result = field.validate(42)
    # then_clause is String, so the result should be a string representation of the int
    assert isinstance(result, str)
    assert result == "42"

def test_if_then_else_else_branch():
    """When the if_clause fails, the else_clause is used."""
    field = IfThenElse(if_clause=Int(), then_clause=String(), else_clause=Bool())
    # Value that does not satisfy Int (e.g., "not an int")
    result = field.validate("not an int")
    # else_clause is Bool, so the result should be a boolean
    assert isinstance(result, bool)
    # Bool field validates any truthy/falsy value; here it should be False
    assert result is False

def test_if_then_else_error_propagation():
    """If the then_clause or else_clause raise an error, it propagates."""
    # then_clause that always raises
    class FailingField(String):
        def validate(self, value):
            raise ValueError("then error")
    field = IfThenElse(if_clause=Int(), then_clause=FailingField(), else_clause=Bool())
    # Value that satisfies Int triggers then_clause, which fails
    with pytest.raises(ValueError, match="then error"):
        field.validate(10)

    # else_clause that always raises
    class FailingElseField(Bool):
        def validate(self, value):
            raise RuntimeError("else error")
    field = IfThenElse(if_clause=Int(), then_clause=String(), else_clause=FailingElseField())
    # Value that fails Int triggers else_clause, which fails
    with pytest.raises(RuntimeError, match="else error"):
        field.validate("bad")
