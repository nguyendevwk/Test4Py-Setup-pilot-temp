import ast as pyast
import typed_ast.ast3 as ast
import pytest
from py_backwards.utils.snippet import find_variables

def test_find_variables_removes_single_let_and_yields_name():
    source = """
def foo():
    let x = 1
    return x
"""
    tree = ast.parse(source)
    names = list(find_variables(tree))
    assert names == ["x"]
    # After removal, the body should contain only the return statement
    body = tree.body[0].body
    assert len(body) == 1
    assert isinstance(body[0], ast.Return)
    # Ensure no remaining let calls
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            assert not (isinstance(node.func, ast.Name) and node.func.id == "let")

def test_find_variables_handles_multiple_lets_and_other_calls():
    source = """
def bar():
    let a = 2
    let b = 3
    print(a, b)
"""
    tree = ast.parse(source)
    names = list(find_variables(tree))
    assert set(names) == {"a", "b"}
    # Body should contain only the print call
    body = tree.body[0].body
    assert len(body) == 1
    assert isinstance(body[0], ast.Expr)
    assert isinstance(body[0].value, ast.Call)
    # No let calls remain
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            assert not (isinstance(node.func, ast.Name) and node.func.id == "let")

def test_find_variables_no_let_calls_leaves_tree_unchanged():
    source = """
def baz():
    x = 5
    y = x + 1
    return y
"""
    tree = ast.parse(source)
    original_source = pyast.unparse(tree)
    names = list(find_variables(tree))
    assert names == []
    # Tree should be unchanged
    new_source = pyast.unparse(tree)
    assert new_source == original_source
