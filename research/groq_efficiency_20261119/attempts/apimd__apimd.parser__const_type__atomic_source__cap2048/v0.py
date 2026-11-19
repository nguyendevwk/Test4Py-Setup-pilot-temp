import ast
import pytest
from apimd.parser import const_type, ANY


def test_const_type_with_basic_constant():
    """Test that a simple numeric constant returns its type name."""
    node = ast.parse("42").body[0].value
    assert isinstance(node, ast.Constant)
    assert const_type(node) == "int"


def test_const_type_with_container_and_element_type():
    """Test that a list of constants returns the correct container type with element type."""
    node = ast.parse("[1, 2, 3]").body[0].value
    assert isinstance(node, ast.List)
    # The function should return 'listint' (lowercase container + element type)
    assert const_type(node) == "listint"


def test_const_type_with_call_and_unsupported_node():
    """Test that a call to a known type returns the type name and an unsupported node returns ANY."""
    call_node = ast.parse("int(3)").body[0].value
    assert isinstance(call_node, ast.Call)
    assert const_type(call_node) == "int"

    name_node = ast.parse("foo").body[0].value
    assert isinstance(name_node, ast.Name)
    assert const_type(name_node) == ANY
