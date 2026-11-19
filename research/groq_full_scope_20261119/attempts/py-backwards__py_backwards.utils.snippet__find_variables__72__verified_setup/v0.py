import ast as pyast
import typed_ast.ast3 as ast
import pytest

from py_backwards.utils.snippet import find_variables
from py_backwards.utils.tree import replace_at, get_non_exp_parent_and_index

def parse_source(source: str) -> ast.Module:
    """Parse source code into a typed_ast Module."""
    return ast.parse(source)

def get_source_code(tree: ast.Module) -> str:
    """Return the source code of the AST (for debugging)."""
    return ast.unparse(tree) if hasattr(ast, "unparse") else None

def test_find_variables_removes_let_and_yields_name(tmp_path):
    source = """
def foo():
    let(x, 10)
    y = x + 5
    print(y)
"""
    tree = parse_source(source)
    vars_found = list(find_variables(tree))
    assert vars_found == ["x"]
    # After removal, the body of foo should not contain the let call
    func_def = tree.body[0]
    assert isinstance(func_def, ast.FunctionDef)
    # The first statement should now be the assignment to y
    first_stmt = func_def.body[0]
    assert isinstance(first_stmt, ast.Assign)
    assert isinstance(first_stmt.targets[0], ast.Name)
    assert first_stmt.targets[0].id == "y"

def test_find_variables_multiple_lets_and_other_calls(tmp_path):
    source = """
def bar():
    let(a, 1)
    let(b, 2)
    z = a + b
    print(z)
    let(c, 3)
"""
    tree = parse_source(source)
    vars_found = list(find_variables(tree))
    assert vars_found == ["a", "b", "c"]
    func_def = tree.body[0]
    # After removal, there should be no Call nodes with func.id == 'let'
    for node in ast.walk(func_def):
        if isinstance(node, ast.Call):
            assert not (isinstance(node.func, ast.Name) and node.func.id == 'let')

def test_find_variables_no_let_calls(tmp_path):
    source = """
def baz():
    x = 5
    y = x * 2
    print(y)
"""
    tree = parse_source(source)
    vars_found = list(find_variables(tree))
    assert vars_found == []
    # Tree should remain unchanged
    func_def = tree.body[0]
    assert isinstance(func_def, ast.FunctionDef)
    assert len(func_def.body) == 3
    assert isinstance(func_def.body[0], ast.Assign)
    assert isinstance(func_def.body[1], ast.Assign)
    assert isinstance(func_def.body[2], ast.Expr)
