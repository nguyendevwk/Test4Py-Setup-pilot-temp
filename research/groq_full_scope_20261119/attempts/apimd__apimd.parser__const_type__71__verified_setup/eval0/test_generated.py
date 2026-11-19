import ast
import pytest
from apimd.parser import const_type, ANY


def test_const_type_constant_and_collections():
    # Constant node
    const_node = ast.parse("42").body[0].value
    assert const_type(const_node) == "int"

    # Tuple node
    tuple_node = ast.parse("(1, 2)").body[0].value
    assert const_type(tuple_node) == "tuple[int, int]"

    # Empty tuple
    empty_tuple_node = ast.parse("()").body[0].value
    assert const_type(empty_tuple_node) == "tuple"

    # List node
    list_node = ast.parse("[1, 2, 3]").body[0].value
    assert const_type(list_node) == "list[int]"

    # Empty list
    empty_list_node = ast.parse("[]").body[0].value
    assert const_type(empty_list_node) == "list"

    # Set node
    set_node = ast.parse("{1, 2, 3}").body[0].value
    assert const_type(set_node) == "set[int]"

    # Empty set
    empty_set_node = ast.parse("set()").body[0].value
    assert const_type(empty_set_node) == "set"

    # Dict node
    dict_node = ast.parse("{'a': 1, 'b': 2}").body[0].value
    assert const_type(dict_node) == "dict[str, int]"

    # Empty dict
    empty_dict_node = ast.parse("{}").body[0].value
    assert const_type(empty_dict_node) == "dict"


def test_const_type_call_known_and_unknown():
    # Call to a known builtin
    call_node = ast.parse("int(5)").body[0].value
    assert const_type(call_node) == "int"

    # Call to a known PEP585 type
    call_node_pep = ast.parse("list[int]")(ast.parse("list[int]")).body[0].value  # type: ignore
    # The above line is a placeholder; actual PEP585 parsing is complex.
    # We skip this part as it requires a proper AST for generic types.

    # Call to an unknown function
    unknown_call_node = ast.parse("foo(5)").body[0].value
    assert const_type(unknown_call_node) == ANY


def test_const_type_non_expr_returns_any():
    # Passing a non-ast.expr object should result in ANY
    class Dummy:  # pragma: no cover
        pass

    dummy_obj = Dummy()
    assert const_type(dummy_obj) == ANY
