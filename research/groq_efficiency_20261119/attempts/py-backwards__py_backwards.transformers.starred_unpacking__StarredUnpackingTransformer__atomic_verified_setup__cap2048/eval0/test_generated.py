import ast as pyast
import typed_ast.ast3 as ast
import pytest
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer

def _parse_and_transform(code: str) -> ast.AST:
    """Parse Python code with typed_ast and apply the transformer."""
    tree = ast.parse(code)
    transformer = StarredUnpackingTransformer()
    transformer.visit(tree)
    return tree

def test_list_with_starred_unpacking():
    """A list containing a starred expression should be transformed into a BinOp."""
    code = "[2, *range(10), 1]"
    tree = _parse_and_transform(code)
    # The top-level node is a Module, its body contains a Expr with a List
    expr = tree.body[0].value
    # After transformation, the List should be replaced by a BinOp
    assert isinstance(expr, ast.BinOp)
    # The left side of the BinOp should be a List([2])
    assert isinstance(expr.left, ast.List)
    assert len(expr.left.elts) == 1
    assert isinstance(expr.left.elts[0], ast.Num) and expr.left.elts[0].n == 2
    # The right side should be a BinOp combining list(range(10)) and [1]
    right = expr.right
    assert isinstance(right, ast.BinOp)
    # The left of the right BinOp should be a Call to list(range(10))
    assert isinstance(right.left, ast.Call)
    assert isinstance(right.left.func, ast.Name) and right.left.func.id == "list"
    # The argument to list should be the Starred value range(10)
    assert isinstance(right.left.args[0], ast.Starred)
    assert isinstance(right.left.args[0].value, ast.Call)
    # The right of the right BinOp should be a List([1])
    assert isinstance(right.right, ast.List)
    assert len(right.right.elts) == 1
    assert isinstance(right.right.elts[0], ast.Num) and right.right.elts[0].n == 1

def test_call_with_starred_unpacking():
    """A function call with starred arguments should be transformed into a single starred argument."""
    code = "print(*range(1), *range(3))"
    tree = _parse_and_transform(code)
    # The top-level node is a Module, its body contains an Expr with a Call
    call = tree.body[0].value
    # After transformation, the Call should have a single starred argument
    assert isinstance(call, ast.Call)
    assert len(call.args) == 1
    arg = call.args[0]
    assert isinstance(arg, ast.Starred)
    # The starred value should be a BinOp combining the two list(range(...)) calls
    binop = arg.value
    assert isinstance(binop, ast.BinOp)
    # Left side of the BinOp should be list(range(1))
    left = binop.left
    assert isinstance(left, ast.Call)
    assert isinstance(left.func, ast.Name) and left.func.id == "list"
    assert isinstance(left.args[0], ast.Starred)
    # Right side of the BinOp should be list(range(3))
    right = binop.right
    assert isinstance(right, ast.Call)
    assert isinstance(right.func, ast.Name) and right.func.id == "list"
    assert isinstance(right.args[0], ast.Starred)

def test_no_starred_unchanged():
    """A list or call without starred expressions should remain unchanged."""
    code = "[1, 2, 3]"
    tree = _parse_and_transform(code)
    expr = tree.body[0].value
    # Should still be a List with three elements
    assert isinstance(expr, ast.List)
    assert len(expr.elts) == 3
    assert all(isinstance(e, ast.Num) for e in expr.elts)

    code_call = "print(1, 2, 3)"
    tree_call = _parse_and_transform(code_call)
    call = tree_call.body[0].value
    # Should still be a Call with three arguments
    assert isinstance(call, ast.Call)
    assert len(call.args) == 3
    assert all(isinstance(a, ast.Num) for a in call.args)
