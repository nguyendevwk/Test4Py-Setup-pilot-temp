import pytest
from pysnooper.variables import needs_parentheses

def test_simple_variable_no_parentheses_needed():
    """A simple variable name should not require parentheses."""
    assert needs_parentheses("a") is False

def test_expression_requires_parentheses():
    """An expression like a+b should require parentheses to access an attribute."""
    assert needs_parentheses("a+b") is True

def test_attribute_access_on_subscript_no_parentheses():
    """Accessing an attribute on a subscripted expression should not require parentheses."""
    assert needs_parentheses("a[0]") is False
