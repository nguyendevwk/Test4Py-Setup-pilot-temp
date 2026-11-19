import pytest
from typing import Dict
from typed_ast import ast3 as ast
from py_backwards.utils.snippet import extend_tree
from py_backwards.utils.tree import find, replace_at, get_non_exp_parent_and_index

def test_extend_tree_replaces_call_with_variable(tmp_path):
    # Prepare source code with an extend call
    src = "x = extend(a)"
    tree = ast.parse(src, filename="<test>")
    # Prepare variables mapping
    variables: Dict[str, ast.AST] = {"a": ast.Name(id="a", ctx=ast.Load())}
    # Apply extend_tree
    extend_tree(tree, variables)
    # After replacement, the Call node should be gone and the value should be the variable node
    # Find the assignment node
    assign = find(tree, ast.Assign)[0]
    # The value of the assignment should be the variable node
    assert isinstance(assign.value, ast.Name)
    assert assign.value.id == "a"
    # Ensure no Call nodes remain
    assert not find(tree, ast.Call)

def test_extend_tree_no_change_when_no_extend_call(tmp_path):
    src = "y = 1"
    tree = ast.parse(src, filename="<test>")
    variables: Dict[str, ast.AST] = {}
    extend_tree(tree, variables)
    # The tree should remain unchanged
    assign = find(tree, ast.Assign)[0]
    assert isinstance(assign.value, ast.Constant)
    assert assign.value.value == 1

def test_extend_tree_raises_key_error_for_missing_variable(tmp_path):
    src = "z = extend(b)"
    tree = ast.parse(src, filename="<test>")
    variables: Dict[str, ast.AST] = {}
    with pytest.raises(KeyError):
        extend_tree(tree, variables)
