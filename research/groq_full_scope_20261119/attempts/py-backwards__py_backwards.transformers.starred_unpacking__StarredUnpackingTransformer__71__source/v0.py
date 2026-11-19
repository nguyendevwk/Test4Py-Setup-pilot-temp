import ast
import typed_ast.ast3 as tast
import pytest
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer

def _parse_and_transform(code: str) -> tast.AST:
    """Parse the code with typed_ast and apply the transformer."""
    tree = tast.parse(code)
    transformer = StarredUnpackingTransformer()
    new_tree = transformer.visit(tree)
    return new_tree

def _ast_dump(node: tast.AST) -> str:
    """Return a deterministic string representation of the AST."""
    return tast.dump(node, annotate_fields=True, include_attributes=False)

def test_starred_unpacking_in_list():
    code = "[2, *range(10), 1]"
    new_tree = _parse_and_transform(code)
    # The top node should be a Module containing a Expr with a BinOp
    module = new_tree
    assert isinstance(module, tast.Module)
    expr = module.body[0]
    assert isinstance(expr, tast.Expr)
    binop = expr.value
    assert isinstance(binop, tast.BinOp)
    # The left side should be a BinOp of [2] + list(range(10))
    left = binop.left
    assert isinstance(left, tast.BinOp)
    assert isinstance(left.left, tast.List)
    assert isinstance(left.right, tast.Call)
    # The right side should be [1]
    right = binop.right
    assert isinstance(right, tast.List)
    # Check that the list elements are correct
    assert [elt.n for elt in left.left.elts] == [2]
    assert right.elts[0].n == 1
    # Ensure the call is list(range(10))
    call = left.right
    assert isinstance(call.func, tast.Name)
    assert call.func.id == "list"
    assert isinstance(call.args[0], tast.Call)
    assert call.args[0].func.id == "range"
    assert call.args[0].args[0].n == 10

def test_starred_unpacking_in_call():
    code = "print(*range(1), *range(3))"
    new_tree = _parse_and_transform(code)
    module = new_tree
    assert isinstance(module, tast.Module)
    expr = module.body[0]
    assert isinstance(expr, tast.Expr)
    call = expr.value
    assert isinstance(call, tast.Call)
    # After transformation, args should be a single Starred wrapping a BinOp
    assert len(call.args) == 1
    starred = call.args[0]
    assert isinstance(starred, tast.Starred)
    binop = starred.value
    assert isinstance(binop, tast.BinOp)
    # Left side: list(range(1))
    left = binop.left
    assert isinstance(left, tast.Call)
    assert left.func.id == "list"
    assert left.args[0].func.id == "range"
    assert left.args[0].args[0].n == 1
    # Right side: list(range(3))
    right = binop.right
    assert isinstance(right, tast.Call)
    assert right.func.id == "list"
    assert right.args[0].func.id == "range"
    assert right.args[0].args[0].n == 3

def test_no_starred_unchanged():
    code = "[1, 2, 3]"
    new_tree = _parse_and_transform(code)
    # The tree should be unchanged; compare dumps
    original_dump = _ast_dump(tast.parse(code))
    new_dump = _ast_dump(new_tree)
    assert original_dump == new_dump
