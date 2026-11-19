import pytest
from pysnooper.variables import needs_parentheses

def test_simple_variable_does_not_need_parentheses():
    # A simple variable name should not require parentheses
    assert needs_parentheses('x') is False

def test_complex_expression_needs_parentheses():
    # An expression that is not a simple name should require parentheses
    assert needs_parentheses('a + b') is True

def test_invalid_source_raises_syntax_error():
    # An empty string is not valid Python code and should raise SyntaxError
    with pytest.raises(SyntaxError):
        needs_parentheses('')
