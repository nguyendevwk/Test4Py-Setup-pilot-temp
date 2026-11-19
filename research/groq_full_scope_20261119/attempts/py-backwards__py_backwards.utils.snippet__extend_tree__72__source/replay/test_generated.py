import pytest
from typing import Dict
from typed_ast import ast3 as ast
from py_backwards.utils.snippet import extend_tree
from py_backwards.utils.tree import find, get_non_exp_parent_and_index, replace_at

def test_extend_tree_replaces_call_with_variable(tmp_path):
    # Create a simple AST with an extend call
    source = "extend(x)"
    tree = ast.parse(source)
    # Prepare a variable mapping
    class DummyVar:
        def __repr__(self):
            return "<DummyVar>"
    variables: Dict[str, DummyVar] = {"x": DummyVar()}
    # Apply extend_tree
    extend_tree(tree, variables)
    # After replacement, the tree should contain the DummyVar instance instead of the Call node
    calls = list(find(tree, ast.Call))
    assert len(calls) == 0  # no Call nodes left
    # The root body should contain the DummyVar
    assert tree.body[0] is variables["x"]

def test_extend_tree_no_extend_call_leaves_tree_unchanged(tmp_path):
    source = "print('hello')"
    tree = ast.parse(source)
    variables: Dict[str, object] = {}
    # Capture the original tree structure
    original_body = list(tree.body)
    extend_tree(tree, variables)
    # The tree should remain unchanged
    assert tree.body == original_body
    assert isinstance(tree.body[0], ast.Expr)

def test_extend_tree_missing_variable_raises_key_error(tmp_path):
    source = "extend(y)"
    tree = ast.parse(source)
    variables: Dict[str, object] = {}  # y not provided
    with pytest.raises(KeyError):
        extend_tree(tree, variables)
