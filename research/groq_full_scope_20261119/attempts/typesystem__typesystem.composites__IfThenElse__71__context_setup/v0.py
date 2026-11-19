import pytest
from typesystem.composites import IfThenElse
from typesystem.fields import Int, String, Any


def test_if_then_else_success():
    """When the if_clause validates, the then_clause is used."""
    field = IfThenElse(if_clause=Int(), then_clause=String())
    # Value 10 passes Int, then String is applied (converts to str)
    result = field.validate(10)
    assert result == "10"
    # Value "hello" fails Int, so else_clause (Any) is used
    result = field.validate("hello")
    assert result == "hello"


def test_if_then_else_else():
    """When the if_clause fails, the else_clause is used."""
    field = IfThenElse(if_clause=Int(), else_clause=String())
    # Value "not an int" fails Int, else_clause String converts to str
    result = field.validate("not an int")
    assert result == "not an int"
    # Value 5 passes Int, then_clause Any is used (identity)
    result = field.validate(5)
    assert result == 5


def test_if_then_else_error_in_then():
    """If the then_clause raises a validation error, it propagates."""
    field = IfThenElse(if_clause=Int(), then_clause=String())
    # Value 3.14 passes Int, but String validation fails (not a string)
    with pytest.raises(ValueError):
        field.validate(3.14)
