import ast
import pytest
from apimd.parser import const_type, ANY

def test_const_type_basic_and_collections():
    # Constant values
    assert const_type(ast.parse("42", mode="eval").body) == "int"
    assert const_type(ast.parse("'hello'", mode="eval").body) == "str"

    # Empty tuple, list, set
    assert const_type(ast.parse("()", mode="eval").body) == "tuple"
    assert const_type(ast.parse("[]", mode="eval").body) == "list"
    assert const_type(ast.parse("set()", mode="eval").body) == "set"

    # Tuple with heterogeneous types
    node = ast.parse("(1, 'a', 3.14)", mode="eval").body
    assert const_type(node) == "tuple[int|str|float]"

    # List with uniform type
    node = ast.parse("[True, False, True]", mode="eval").body
    assert const_type(node) == "list[bool]"

    # Set with uniform type
    node = ast.parse("{1, 2, 3}", mode="eval").body
    assert const_type(node) == "set[int]"

    # Dict with uniform key/value types
    node = ast.parse("{'x': 1, 'y': 2}", mode="eval").body
    assert const_type(node) == "dict[str|int]"

def test_const_type_call_and_pep585():
    # Direct built-in type calls
    node = ast.parse("int()", mode="eval").body
    assert const_type(node) == "int"

    # PEP585 type hint call
    node = ast.parse("list[int]()", mode="eval").body
    # The unparse of the func will be 'list[int]', which is in PEP585 keys
    assert const_type(node) == "list[int]"

    # Attribute call that is not a known type
    node = ast.parse("math.sqrt(4)", mode="eval").body
    assert const_type(node) == ANY

def test_const_type_error_and_boundary():
    # Unsupported node type should return ANY
    node = ast.parse("x + y", mode="eval").body
    assert const_type(node) == ANY

    # Empty dict
    node = ast.parse("{}", mode="eval").body
    assert const_type(node) == "dict"

    # Dict with mixed key/value types
    node = ast.parse("{1: 'a', 2: 'b'}", mode="eval").body
    assert const_type(node) == "dict[int|str]"
