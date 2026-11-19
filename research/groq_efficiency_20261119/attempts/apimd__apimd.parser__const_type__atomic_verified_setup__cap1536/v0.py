import ast
import pytest
from apimd.parser import const_type, ANY


def test_constant_type_inference():
    """Test that literal constants are inferred correctly."""
    # Integer literal
    node_int = ast.parse("42", mode="eval").body
    assert const_type(node_int) == "int"

    # String literal
    node_str = ast.parse("'hello'", mode="eval").body
    assert const_type(node_str) == "str"

    # Boolean literal
    node_bool = ast.parse("True", mode="eval").body
    assert const_type(node_bool) == "bool"

    # None literal
    node_none = ast.parse("None", mode="eval").body
    # None is not a Constant in Python 3.8+, but in 3.9+ it is a Constant with value None
    # The function should return 'NoneType' via _type_name
    assert const_type(node_none) == "NoneType"


def test_sequence_and_dict_type_inference():
    """Test that sequences and dictionaries are inferred with element types."""
    # List of integers
    node_list = ast.parse("[1, 2, 3]", mode="eval").body
    assert const_type(node_list) == "list[int]"

    # Tuple of mixed types
    node_tuple = ast.parse("(1, 'a', True)", mode="eval").body
    assert const_type(node_tuple) == "tuple[int, str, bool]"

    # Set of floats
    node_set = ast.parse("{1.0, 2.5}", mode="eval").body
    assert const_type(node_set) == "set[float]"

    # Dict with string keys and integer values
    node_dict = ast.parse("{'x': 1, 'y': 2}", mode="eval").body
    assert const_type(node_dict) == "dict[str, int]"

    # Empty list should default to list[Any]
    node_empty_list = ast.parse("[]", mode="eval").body
    assert const_type(node_empty_list) == "list[Any]"


def test_call_and_unknown_type_inference():
    """Test that function calls to known constructors are inferred and unknown calls return ANY."""
    # Call to int constructor
    node_call_int = ast.parse("int(5)", mode="eval").body
    assert const_type(node_call_int) == "int"

    # Call to a custom function not in known set
    node_call_custom = ast.parse("my_func(10)", mode="eval").body
    assert const_type(node_call_custom) == ANY

    # Call to a built-in that is not a type constructor
    node_call_print = ast.parse("print('test')", mode="eval").body
    assert const_type(node_call_print) == ANY
