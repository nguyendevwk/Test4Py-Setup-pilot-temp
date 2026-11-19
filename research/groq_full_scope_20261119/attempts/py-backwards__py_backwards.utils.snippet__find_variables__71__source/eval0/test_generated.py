import ast as pyast
import typed_ast.ast3 as ast
import pytest
from py_backwards.utils.snippet import find_variables
from py_backwards.utils.tree import find, get_non_exp_parent_and_index, replace_at

def test_find_variables_removes_single_let_and_yields_name():
    source = """
def foo():
    let x = 1
    return x
"""
    tree = ast.parse(source)
    vars = list(find_variables(tree))
    assert vars == ["x"]
    # The let call should be removed from the function body
    func_body = tree.body[0].body
    assert all(not isinstance(node, ast.Call) or node.func.id != "let" for node in func_body)
    # The remaining body should contain only the return statement
    assert len(func_body) == 1
    assert isinstance(func_body[0], ast.Return)

def test_find_variables_handles_multiple_lets_and_preserves_order():
    source = """
def bar():
    let a = 1
    let b = 2
    return a + b
"""
    tree = ast.parse(source)
    vars = list(find_variables(tree))
    assert vars == ["a", "b"]
    # Both let calls should be removed
    func_body = tree.body[0].body
    assert all(not isinstance(node, ast.Call) or node.func.id != "let" for node in func_body)
    # The remaining body should contain only the return statement
    assert len(func_body) == 1
    assert isinstance(func_body[0], ast.Return)

def test_find_variables_raises_on_invalid_let_argument():
    source = """
def baz():
    let (x, y) = (1, 2)
    return x
"""
    tree = ast.parse(source)
    # The first argument to let is a Tuple, not a Name, so accessing .id should raise AttributeError
    with pytest.raises(AttributeError):
        list(find_variables(tree))
