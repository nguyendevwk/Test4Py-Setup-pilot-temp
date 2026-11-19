import ast as pyast
import typed_ast.ast3 as ast
import pytest
from py_backwards.utils.snippet import find_variables
from py_backwards.utils.tree import find, get_non_exp_parent_and_index, replace_at

def test_find_variables_removes_and_yields_names():
    source = """
def foo():
    let(x, 1)
    y = x + 2
    let(z, 3)
    return y
"""
    tree = ast.parse(source)
    vars_found = list(find_variables(tree))
    assert vars_found == ["x", "z"]
    # Ensure the let calls are removed from the function body
    func_body = tree.body[0].body
    for node in func_body:
        assert not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and
                    isinstance(node.value.func, ast.Name) and node.value.func.id == "let")

def test_find_variables_no_let_calls():
    source = """
def bar():
    a = 1
    b = a + 2
    return b
"""
    tree = ast.parse(source)
    vars_found = list(find_variables(tree))
    assert vars_found == []
    # Body should remain unchanged
    func_body = tree.body[0].body
    assert len(func_body) == 3
    assert isinstance(func_body[0], ast.Assign)
    assert isinstance(func_body[1], ast.Assign)
    assert isinstance(func_body[2], ast.Return)

def test_find_variables_let_with_non_name_argument_raises():
    source = """
def baz():
    let(5, 10)
    return 0
"""
    tree = ast.parse(source)
    with pytest.raises(AttributeError):
        list(find_variables(tree))
