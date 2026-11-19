import pytest
from pysnooper.variables import needs_parentheses

def test_simple_variable_no_parentheses_needed():
    """
    For a simple variable name, adding parentheses around the source
    should not change the compiled bytecode.
    """
    assert needs_parentheses("a") is False

def test_expression_parentheses_needed():
    """
    For an expression that is not a simple name, parentheses are required
    to preserve the intended attribute access order.
    """
    assert needs_parentheses("a + b") is True
    assert needs_parentheses("f()") is True

def test_invalid_source_raises_syntax_error():
    """
    An invalid source string should raise a SyntaxError during compilation.
    """
    with pytest.raises(SyntaxError):
        needs_parentheses("a +")
