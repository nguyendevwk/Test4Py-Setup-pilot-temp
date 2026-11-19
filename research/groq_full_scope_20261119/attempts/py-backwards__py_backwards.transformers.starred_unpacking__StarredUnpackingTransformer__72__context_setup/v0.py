import pytest
from typed_ast import ast3 as ast
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer

def _parse_and_transform(code: str) -> ast.AST:
    """Parse the code with typed_ast and apply the transformer."""
    tree = ast.parse(code)
    transformer = StarredUnpackingTransformer()
    transformer.visit(tree)
    return tree

def test_list_with_starred_unpacking():
    code = "[2, *range(10), 1]"
    tree = _parse_and_transform(code)
    # The root should be a Module with one Expr containing a BinOp
    assert isinstance(tree, ast.Module)
    expr = tree.body[0]
    assert isinstance(expr, ast.Expr)
    binop = expr.value
    assert isinstance(binop, ast.BinOp)
    # Left side should be a BinOp of [2] + list(range(10))
    left = binop.left
    assert isinstance(left, ast.BinOp)
    assert isinstance(left.left, ast.List)
    assert isinstance(left.right, ast.Call)
    assert left.right.func.id == "list"
    # Right side should be [1]
    right = binop.right
    assert isinstance(right, ast.List)

def test_call_with_starred_unpacking():
    code = "print(*range(1), *range(3))"
    tree = _parse_and_transform(code)
    # The root should be a Module with one Expr containing a Call
    assert isinstance(tree, ast.Module)
    expr = tree.body[0]
    assert isinstance(expr, ast.Expr)
    call = expr.value
    assert isinstance(call, ast.Call)
    # The call should have one argument: a Starred wrapping a BinOp
    assert len(call.args) == 1
    starred = call.args[0]
    assert isinstance(starred, ast.Starred)
    binop = starred.value
    assert isinstance(binop, ast.BinOp)
    # The BinOp should combine two list calls
    assert isinstance(binop.left, ast.Call)
    assert isinstance(binop.right, ast.Call)
    assert binop.left.func.id == "list"
    assert binop.right.func.id == "list"

def test_no_starred_list_remains_unchanged():
    code = "[1, 2, 3]"
    tree = _parse_and_transform(code)
    # The tree should be unchanged: a Module with one Expr containing a List
    assert isinstance(tree, ast.Module)
    expr = tree.body[0]
    assert isinstance(expr, ast.Expr)
    lst = expr.value
    assert isinstance(lst, ast.List)
    # The list elements should be the same as parsed
    elts = [elt.id if isinstance(elt, ast.Name) else elt.n for elt in lst.elts]
    assert elts == [1, 2, 3]
