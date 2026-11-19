import pytest
from pysnooper.variables import needs_parentheses

def test_simple_variable_does_not_need_parentheses():
    # A plain variable name should not require parentheses
    assert needs_parentheses("a") is False

def test_expression_needs_parentheses():
    # An expression like a function call needs parentheses to access an attribute
    # e.g., "f().x" vs "(f()).x" produce different bytecode
    assert needs_parentheses("f()") is True

def test_invalid_source_raises_syntax_error():
    # Passing an incomplete expression should raise a SyntaxError
    with pytest.raises(SyntaxError):
        needs_parentheses("1+")
