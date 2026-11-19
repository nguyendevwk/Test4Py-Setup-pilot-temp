import ast
import pytest
from apimd.parser import const_type, ANY

def test_const_type_basic_literals():
    # Integer literal
    node = ast.parse("42", mode="eval").body
    assert const_type(node) == "int"

    # String literal
    node = ast.parse("'hello'", mode="eval").body
    assert const_type(node) == "str"

    # Boolean literal
    node = ast.parse("True", mode="eval").body
    assert const_type(node) == "bool"

def test_const_type_collections_and_calls(tmp_path):
    # Empty tuple
    node = ast.parse("()", mode="eval").body
    assert const_type(node) == "tuple"

    # Tuple of ints
    node = ast.parse("(1, 2, 3)", mode="eval").body
    assert const_type(node) == "tuple[int]"

    # List of strings
    node = ast.parse("['a', 'b']", mode="eval").body
    assert const_type(node) == "list[str]"

    # Set of floats
    node = ast.parse("{1.0, 2.0}", mode="eval").body
    assert const_type(node) == "set[float]"

    # Dict with int keys and str values
    node = ast.parse("{1: 'a', 2: 'b'}", mode="eval").body
    assert const_type(node) == "dict[int, str]"

    # Call to built-in type
    node = ast.parse("int()", mode="eval").body
    assert const_type(node) == "int"

    # Call to PEP585 type alias
    node = ast.parse("list[int]()", mode="eval").body
    assert const_type(node) == "list"

def test_const_type_unknown_and_error():
    # Unsupported node type (e.g., a function definition)
    node = ast.parse("def f(): pass", mode="exec").body[0]
    assert const_type(node) == ANY

    # Call to unknown function
    node = ast.parse("unknown_func()", mode="eval").body
    assert const_type(node) == ANY
