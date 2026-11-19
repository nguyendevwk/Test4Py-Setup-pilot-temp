import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer

def _parse_and_transform(source: str) -> ast.AST:
    """Parse source with typed_ast and apply the transformer."""
    tree = typed_ast.parse(source)
    transformer = StarredUnpackingTransformer()
    transformed = transformer.visit(tree)
    return transformed

def test_list_with_starred_is_transformed_to_binop():
    source = "[2, *range(10), 1]"
    transformed = _parse_and_transform(source)
    # The top-level node is a Module with a single Expr
    expr = transformed.body[0].value
    # After transformation, the Expr should be a BinOp
    assert isinstance(expr, typed_ast.BinOp)
    # The left side should be a BinOp (2 + list(range(10)))
    left = expr.left
    assert isinstance(left, typed_ast.BinOp)
    assert isinstance(left.left, typed_ast.List)
    assert isinstance(left.right, typed_ast.Call)
    # The right side should be a List containing the final element
    assert isinstance(expr.right, typed_ast.List)
    # Ensure the final element is the integer 1
    assert isinstance(expr.right.elts[0], typed_ast.Num)
    assert expr.right.elts[0].n == 1

def test_call_with_starred_arguments_is_wrapped_in_starred():
    source = "print(*range(1), *range(3))"
    transformed = _parse_and_transform(source)
    # The top-level node is a Module with a single Expr
    expr = transformed.body[0].value
    # After transformation, the Expr should be a Call
    assert isinstance(expr, typed_ast.Call)
    # The call should have a single argument which is a Starred
    assert len(expr.args) == 1
    starred = expr.args[0]
    assert isinstance(starred, typed_ast.Starred)
    # The starred value should be a BinOp representing the sum of two lists
    binop = starred.value
    assert isinstance(binop, typed_ast.BinOp)
    # Each side of the BinOp should be a List
    assert isinstance(binop.left, typed_ast.List)
    assert isinstance(binop.right, typed_ast.List)

def test_normal_list_without_starred_remains_unchanged():
    source = "[1, 2, 3]"
    transformed = _parse_and_transform(source)
    # The top-level node is a Module with a single Expr
    expr = transformed.body[0].value
    # It should still be a List with the same elements
    assert isinstance(expr, typed_ast.List)
    elts = expr.elts
    assert len(elts) == 3
    assert all(isinstance(e, typed_ast.Num) for e in elts)
    assert [e.n for e in elts] == [1, 2, 3]
