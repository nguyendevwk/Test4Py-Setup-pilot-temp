import pytest
from pysnooper.variables import needs_parentheses

def test_simple_variable_does_not_need_parentheses(tmp_path):
    # A plain variable should not require parentheses
    assert needs_parentheses("a") is False
    # The bytecode for accessing an attribute is identical with or without parentheses
    assert needs_parentheses("my_obj") is False

def test_expression_needs_parentheses(tmp_path):
    # An expression like a function call needs parentheses to access an attribute
    # e.g., "func().x" vs "(func()).x" produce different bytecode
    assert needs_parentheses("func()") is True
    # A more complex expression also requires parentheses
    assert needs_parentheses("a + b") is True

def test_invalid_source_raises_syntax_error(tmp_path):
    # Passing an incomplete expression should raise a SyntaxError
    with pytest.raises(SyntaxError):
        needs_parentheses("1 +")
