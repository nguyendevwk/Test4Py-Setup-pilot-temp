import ast
import pytest
from apimd.parser import const_type, ANY

def test_constant_type_inference():
    # Integer constant
    node = ast.parse("42", mode="eval").body
    assert const_type(node) == "int"

    # String constant
    node = ast.parse("'hello'", mode="eval").body
    assert const_type(node) == "str"

    # None constant
    node = ast.parse("None", mode="eval").body
    assert const_type(node) == "NoneType"

def test_sequence_and_dict_type_inference():
    # List of integers
    node = ast.parse("[1, 2, 3]", mode="eval").body
    assert const_type(node) == "list[int]"

    # Tuple of mixed types
    node = ast.parse("(1, 'a', 3.14)", mode="eval").body
    assert const_type(node) == "tuple[int, str, float]"

    # Set of strings
    node = ast.parse("{'x', 'y'}", mode="eval").body
    assert const_type(node) == "set[str]"

    # Dict with int keys and str values
    node = ast.parse("{1: 'a', 2: 'b'}", mode="eval").body
    assert const_type(node) == "dict[int, str]"

def test_call_and_default_behavior():
    # Call to built-in type constructor
    node = ast.parse("int(5)", mode="eval").body
    assert const_type(node) == "int"

    # Call to unknown function
    node = ast.parse("foo(1)", mode="eval").body
    assert const_type(node) == ANY

    # Non-ast.expr input should return ANY
    with pytest.raises(AttributeError):
        # Passing a string instead of an AST node triggers an AttributeError
        const_type("not an expr")
