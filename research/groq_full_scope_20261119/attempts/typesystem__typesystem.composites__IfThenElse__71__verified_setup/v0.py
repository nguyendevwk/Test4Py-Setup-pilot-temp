import pytest
from typesystem.composites import IfThenElse
from typesystem.fields import Int, String, Any


def test_if_then_else_success():
    """When the if_clause validates, the then_clause is used."""
    field = IfThenElse(if_clause=Int(), then_clause=String())
    # Value 10 passes Int, then String is applied (converts to str)
    result = field.validate(10)
    assert isinstance(result, str)
    assert result == "10"


def test_if_then_else_else():
    """When the if_clause fails, the else_clause is used."""
    field = IfThenElse(if_clause=Int(), else_clause=String())
    # Value "not an int" fails Int, so String is applied
    result = field.validate("not an int")
    assert isinstance(result, str)
    assert result == "not an int"


def test_if_then_else_error_in_then():
    """If the then_clause raises an error, it propagates."""
    field = IfThenElse(if_clause=Int(), then_clause=String())
    # Value 10 passes Int, but String.validate will raise if value is not a string
    # Since 10 is int, String.validate will raise a ValidationError
    with pytest.raises(Exception):
        field.validate(10)
