import ast
import pytest
from apimd.parser import const_type, ANY


def test_constant_and_container_types():
    # Constant
    const_node = ast.parse("42").body[0].value
    assert const_type(const_node) == "int"

    # Tuple
    tuple_node = ast.parse("(1, 2)").body[0].value
    assert const_type(tuple_node) == "tuple[int, int]"

    # Empty tuple
    empty_tuple_node = ast.parse("()").body[0].value
    assert const_type(empty_tuple_node) == "tuple[]"

    # List
    list_node = ast.parse("[1, 2, 3]").body[0].value
    assert const_type(list_node) == "list[int]"

    # Empty list
    empty_list_node = ast.parse("[]").body[0].value
    assert const_type(empty_list_node) == "list[]"

    # Set
    set_node = ast.parse("{1, 2, 3}").body[0].value
    assert const_type(set_node) == "set[int]"

    # Empty set
    empty_set_node = ast.parse("set()").body[0].value
    assert const_type(empty_set_node) == "set[]"

    # Dict
    dict_node = ast.parse("{'a': 1, 'b': 2}").body[0].value
    assert const_type(dict_node) == "dict[str, int]"

    # Empty dict
    empty_dict_node = ast.parse("{}").body[0].value
    assert const_type(empty_dict_node) == "dict[]"


def test_call_and_unknown_call():
    # Known call
    call_node = ast.parse("int(5)").body[0].value
    assert const_type(call_node) == "int"

    # Known call with PEP585 type
    call_node_pep = ast.parse("list[int]([1, 2])").body[0].value
    # The unparse of the func will be 'list[int]', which is in PEP585 keys
    assert const_type(call_node_pep) == "list[int]"

    # Unknown call
    unknown_call_node = ast.parse("foo(5)").body[0].value
    assert const_type(unknown_call_node) == ANY


def test_non_constant_expr_returns_any():
    # Name expression (not a constant)
    name_node = ast.parse("x").body[0].value
    assert const_type(name_node) == ANY

    # Attribute expression
    attr_node = ast.parse("obj.attr").body[0].value
    assert const_type(attr_node) == ANY

    # Binary operation
    binop_node = ast.parse("1 + 2").body[0].value
    assert const_type(binop_node) == ANY
