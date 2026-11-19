import ast
import pytest
from apimd.parser import const_type, ANY


def test_constant_and_sequence_types():
    # Integer constant
    node_int = ast.parse("42", mode="eval").body
    assert const_type(node_int) == "int"

    # Tuple of two strings
    node_tuple = ast.parse("('a', 'b')", mode="eval").body
    # Expected: 'tuplestr' (tuple + element type)
    assert const_type(node_tuple) == "tuplestr"

    # List of mixed types: int and float
    node_list = ast.parse("[1, 2.5]", mode="eval").body
    # Expected: 'listint' because element type is inferred from first element
    assert const_type(node_list) == "listint"

    # Set of booleans
    node_set = ast.parse("{True, False}", mode="eval").body
    assert const_type(node_set) == "setbool"

    # Dict with string keys and integer values
    node_dict = ast.parse("{'x': 10, 'y': 20}", mode="eval").body
    assert const_type(node_dict) == "dictstrint"


def test_call_and_unknown_cases():
    # Call to built-in int constructor
    node_call_int = ast.parse("int('123')", mode="eval").body
    assert const_type(node_call_int) == "int"

    # Call to a function not in the allowed set
    node_call_unknown = ast.parse("custom_func(5)", mode="eval").body
    assert const_type(node_call_unknown) == ANY

    # Call to a method that is not a simple name or attribute
    node_call_complex = ast.parse("(lambda x: x)(5)", mode="eval").body
    assert const_type(node_call_complex) == ANY


def test_invalid_input_returns_any():
    # Passing a non-ast.expr object should fall through to the default case
    assert const_type(123) == ANY
    assert const_type("not an expr") == ANY
