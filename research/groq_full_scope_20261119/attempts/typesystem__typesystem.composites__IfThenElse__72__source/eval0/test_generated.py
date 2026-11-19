import pytest
from typesystem.composites import IfThenElse
from typesystem.fields import Any, Int, String


def test_if_then_else_success():
    """
    When the if_clause validates, the then_clause should be used.
    """
    field = IfThenElse(if_clause=Int(), then_clause=String())
    # Value 42 satisfies Int, so String validation should succeed (any string accepted)
    result = field.validate(42)
    assert result == 42  # String() returns the original value if it is a string, else raises
    # Now test with a string that satisfies String()
    result = field.validate("hello")
    assert result == "hello"


def test_if_then_else_else_path():
    """
    When the if_clause fails, the else_clause should be used.
    """
    field = IfThenElse(if_clause=Int(), else_clause=String())
    # Value "not an int" fails Int, so String validation should succeed
    result = field.validate("not an int")
    assert result == "not an int"
    # Value 3.14 fails Int, should also go to else_clause
    result = field.validate(3.14)
    assert result == 3.14


def test_if_then_else_error_on_then():
    """
    If the then_clause validation fails, the error should propagate.
    """
    # then_clause expects a string, but we pass an int
    field = IfThenElse(if_clause=Int(), then_clause=String())
    with pytest.raises(Exception):
        field.validate(123)  # 123 passes Int, then String() should raise
