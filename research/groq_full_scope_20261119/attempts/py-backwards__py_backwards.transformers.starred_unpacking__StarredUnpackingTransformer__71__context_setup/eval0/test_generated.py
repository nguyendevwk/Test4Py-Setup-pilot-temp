import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer

def _parse_and_transform(code: str) -> ast.AST:
    """Parse the code with typed_ast and apply the transformer."""
    tree = ast.parse(code)
    transformer = StarredUnpackingTransformer()
    transformer.visit(tree)
    return tree

def test_starred_in_list_transforms_to_sum_of_lists():
    code = "[2, *range(10), 1]"
    tree = _parse_and_transform(code)
    # The top node should be a Module with a single Expr whose value is a BinOp
    expr = tree.body[0].value
    assert isinstance(expr, ast.BinOp)
    # Left side should be a BinOp of [2] + list(range(10))
    left = expr.left
    assert isinstance(left, ast.BinOp)
    assert isinstance(left.left, ast.List) and left.left.elts[0].n == 2
    assert isinstance(left.right, ast.Call) and left.right.func.id == "list"
    # Right side should be a List with [1]
    assert isinstance(expr.right, ast.List) and expr.right.elts[0].n == 1

def test_starred_in_call_transforms_to_single_starred_argument():
    code = "print(*range(1), *range(3))"
    tree = _parse_and_transform(code)
    call = tree.body[0].value
    assert isinstance(call, ast.Call)
    # After transformation, there should be exactly one argument which is a Starred
    assert len(call.args) == 1
    starred = call.args[0]
    assert isinstance(starred, ast.Starred)
    # The starred value should be a BinOp combining two list calls
    binop = starred.value
    assert isinstance(binop, ast.BinOp)
    # Left side: list(range(1))
    assert isinstance(binop.left, ast.Call) and binop.left.func.id == "list"
    # Right side: list(range(3))
    assert isinstance(binop.right, ast.Call) and binop.right.func.id == "list"

def test_non_starred_list_remains_unchanged():
    code = "[1, 2, 3]"
    tree = _parse_and_transform(code)
    expr = tree.body[0].value
    # Should still be a List node with the same elements
    assert isinstance(expr, ast.List)
    assert [elt.n for elt in expr.elts] == [1, 2, 3]
