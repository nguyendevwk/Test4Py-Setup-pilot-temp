import pytest
from typing import Dict
from typed_ast import ast3 as ast
from py_backwards.utils.snippet import extend_tree

# Helper to parse source into an AST
def parse_source(src: str) -> ast.AST:
    return ast.parse(src)

def test_extend_tree_replaces_call_with_ast_nodes():
    # Original code contains a call to extend('x')
    src = "extend('x')"
    tree = parse_source(src)

    # Variable mapping: 'x' -> list of AST nodes to insert
    var_node = ast.Expr(value=ast.Constant(value=42))
    variables: Dict[str, ast.AST] = {"x": [var_node]}

    extend_tree(tree, variables)

    # After transformation, the tree should contain the constant 42 instead of the call
    # The top-level body should have one Expr node with Constant 42
    assert len(tree.body) == 1
    expr_node = tree.body[0]
    assert isinstance(expr_node, ast.Expr)
    assert isinstance(expr_node.value, ast.Constant)
    assert expr_node.value.value == 42

def test_extend_tree_multiple_calls_and_variable_as_ast():
    # Code with two extend calls
    src = """
extend('a')
extend('b')
"""
    tree = parse_source(src)

    # Variables mapping: 'a' -> AST node, 'b' -> list of AST nodes
    var_a = ast.Expr(value=ast.Constant(value="hello"))
    var_b = [ast.Expr(value=ast.Constant(value=99))]
    variables: Dict[str, ast.AST] = {"a": var_a, "b": var_b}

    extend_tree(tree, variables)

    # After transformation, the body should contain the two inserted nodes
    assert len(tree.body) == 2
    first, second = tree.body
    assert isinstance(first, ast.Expr)
    assert isinstance(first.value, ast.Constant)
    assert first.value.value == "hello"
    assert isinstance(second, ast.Expr)
    assert isinstance(second.value, ast.Constant)
    assert second.value.value == 99

def test_extend_tree_missing_variable_raises_key_error():
    src = "extend('missing')"
    tree = parse_source(src)
    variables: Dict[str, ast.AST] = {}

    with pytest.raises(KeyError):
        extend_tree(tree, variables)
