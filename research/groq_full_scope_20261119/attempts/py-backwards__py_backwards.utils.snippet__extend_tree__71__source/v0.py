import pytest
from typing import Dict
from typed_ast import ast3 as ast
from py_backwards.utils.snippet import extend_tree
from py_backwards.utils.tree import find, get_non_exp_parent_and_index, replace_at

# Dummy Variable class used by extend_tree
class Variable:
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return f"Variable({self.name!r})"

def build_ast(source: str) -> ast.AST:
    """Parse source code into a typed_ast AST."""
    return ast.parse(source, mode="exec")

def test_extend_tree_replaces_call_with_variable(tmp_path):
    """Normal case: extend call is replaced by the corresponding variable."""
    source = "x = extend(a)"
    tree = build_ast(source)
    variables: Dict[str, Variable] = {"a": Variable("a")}
    extend_tree(tree, variables)

    # After transformation, the body should contain the Variable instance instead of Call
    body = tree.body[0]
    assert isinstance(body, ast.Assign)
    assert isinstance(body.value, Variable)
    assert body.value.name == "a"

def test_extend_tree_no_change_when_no_extend_call(tmp_path):
    """Boundary case: tree without extend calls remains unchanged."""
    source = "y = 1 + 2"
    tree = build_ast(source)
    variables: Dict[str, Variable] = {}
    extend_tree(tree, variables)

    # The tree should still contain the original BinOp node
    body = tree.body[0]
    assert isinstance(body, ast.Assign)
    assert isinstance(body.value, ast.BinOp)
    assert isinstance(body.value.left, ast.Num)
    assert isinstance(body.value.right, ast.Num)

def test_extend_tree_raises_key_error_for_missing_variable(tmp_path):
    """Error case: missing variable in the mapping raises KeyError."""
    source = "z = extend(b)"
    tree = build_ast(source)
    variables: Dict[str, Variable] = {}  # 'b' not provided

    with pytest.raises(KeyError):
        extend_tree(tree, variables)
