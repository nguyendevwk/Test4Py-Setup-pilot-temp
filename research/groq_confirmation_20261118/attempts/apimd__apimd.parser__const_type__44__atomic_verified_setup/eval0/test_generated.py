import ast
import pytest
from apimd.parser import const_type
from apimd.pep585 import PEP585

def test_const_type_basic_literals():
    # Integer literal
    node_int = ast.parse("42", mode="eval").body
    assert const_type(node_int) == "int"

    # String literal
    node_str = ast.parse("'hello'", mode="eval").body
    assert const_type(node_str) == "str"

    # Boolean literal
    node_bool = ast.parse("True", mode="eval").body
    assert const_type(node_bool) == "bool"

    # None literal should fall back to ANY
    node_none = ast.parse("None", mode="eval").body
    assert const_type(node_none) == "ANY"

def test_const_type_collections_and_pep585():
    # List of integers
    node_list = ast.parse("[1, 2, 3]", mode="eval").body
    assert const_type(node_list) == "listint"

    # Tuple of mixed types
    node_tuple = ast.parse("(1, 'a', 3.14)", mode="eval").body
    assert const_type(node_tuple) == "tupleintstrfloat"

    # Set of strings
    node_set = ast.parse("{'x', 'y'}", mode="eval").body
    assert const_type(node_set) == "setstr"

    # Dict with int keys and str values
    node_dict = ast.parse("{1: 'one', 2: 'two'}", mode="eval").body
    assert const_type(node_dict) == "dictintstr"

    # PEP585 type hint: list[int]
    node_pep = ast.parse("list[int]", mode="eval").body
    assert const_type(node_pep) == "listint"

    # PEP585 type hint: dict[str, float]
    node_pep2 = ast.parse("dict[str, float]", mode="eval").body
    assert const_type(node_pep2) == "dictstrfloat"

def test_const_type_call_and_unknown():
    # Call to a known builtin type
    node_call = ast.parse("int(5)", mode="eval").body
    assert const_type(node_call) == "int"

    # Call to an unknown function
    node_call_unknown = ast.parse("foo(1, 2)", mode="eval").body
    assert const_type(node_call_unknown) == "ANY"

    # Call to a function that is a PEP585 alias
    node_call_pep = ast.parse("list[int](1, 2, 3)", mode="eval").body
    # The function name is parsed as a Call to an Attribute, which is not handled,
    # so it should fall back to ANY
    assert const_type(node_call_pep) == "ANY"
