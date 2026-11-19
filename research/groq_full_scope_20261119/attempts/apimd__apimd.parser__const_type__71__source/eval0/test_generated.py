import ast
import pytest
from apimd.parser import const_type, ANY


def test_const_type_basic_literals():
    # Constant nodes
    assert const_type(ast.parse("42", mode="eval").body) == "int"
    assert const_type(ast.parse("3.14", mode="eval").body) == "float"
    assert const_type(ast.parse("'hello'", mode="eval").body) == "str"
    assert const_type(ast.parse("True", mode="eval").body) == "bool"
    assert const_type(ast.parse("None", mode="eval").body) == "NoneType"


def test_const_type_collections_and_pep585():
    # Empty and non‑empty collections
    assert const_type(ast.parse("()", mode="eval").body) == "tuple"
    assert const_type(ast.parse("[1, 2, 3]", mode="eval").body) == "listint"
    assert const_type(ast.parse("{1, 2, 3}", mode="eval").body) == "setint"
    assert const_type(ast.parse("{'a': 1, 'b': 2}", mode="eval").body) == "dictstrint"

    # PEP585 type constructors
    assert const_type(ast.parse("list[int]", mode="eval").body) == "listint"
    assert const_type(ast.parse("dict[str, float]", mode="eval").body) == "dictstrfloat"
    assert const_type(ast.parse("tuple[int, str]", mode="eval").body) == "tupleintstr"


def test_const_type_unhandled_nodes_returns_any():
    # Unsupported node types should fall back to ANY
    assert const_type(ast.parse("x + y", mode="eval").body) == ANY
    assert const_type(ast.parse("def f(): pass", mode="exec").body[0]) == ANY
    assert const_type(ast.parse("class C: pass", mode="exec").body[0]) == ANY
