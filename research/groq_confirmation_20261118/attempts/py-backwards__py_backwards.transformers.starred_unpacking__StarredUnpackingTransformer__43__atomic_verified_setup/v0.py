import ast as pyast
import typed_ast.ast3 as ast
import pytest
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer

def parse_and_transform(source: str) -> ast.AST:
    """Parse source with typed_ast and apply StarredUnpackingTransformer."""
    tree = ast.parse(source)
    transformer = StarredUnpackingTransformer()
    transformer.visit(tree)
    return tree

def ast_dump(node: ast.AST) -> str:
    """Return a deterministic string representation of an AST node."""
    return ast.dump(node, annotate_fields=True, include_attributes=False)

def test_list_with_starred_unpacking():
    source = "[2, *range(10), 1]"
    tree = parse_and_transform(source)
    # The root should be a Module containing a single Expr with a BinOp
    expr = tree.body[0].value
    assert isinstance(expr, ast.BinOp)
    # Left side should be a BinOp of List([2]) + Call(list, [range(10)])
    left = expr.left
    assert isinstance(left, ast.BinOp)
    assert isinstance(left.left, ast.List)
    assert len(left.left.elts) == 1 and isinstance(left.left.elts[0], ast.Num) and left.left.elts[0].n == 2
    assert isinstance(left.right, ast.Call)
    assert isinstance(left.right.func, ast.Name) and left.right.func.id == "list"
    assert isinstance(left.right.args[0], ast.Starred)
    # Right side should be List([1])
    right = expr.right
    assert isinstance(right, ast.List)
    assert len(right.elts) == 1 and isinstance(right.elts[0], ast.Num) and right.elts[0].n == 1

def test_call_with_starred_unpacking():
    source = "print(*range(1), *range(3))"
    tree = parse_and_transform(source)
    # The root should be a Module containing a single Expr with a Call
    call = tree.body[0].value
    assert isinstance(call, ast.Call)
    assert isinstance(call.func, ast.Name) and call.func.id == "print"
    # After transformation, there should be a single starred argument
    assert len(call.args) == 1
    starred = call.args[0]
    assert isinstance(starred, ast.Starred)
    # The starred value should be a BinOp of two list calls
    binop = starred.value
    assert isinstance(binop, ast.BinOp)
    assert isinstance(binop.left, ast.Call)
    assert isinstance(binop.right, ast.Call)
    # Each call should be list(range(...))
    for call_part in (binop.left, binop.right):
        assert isinstance(call_part.func, ast.Name) and call_part.func.id == "list"
        assert isinstance(call_part.args[0], ast.Starred)
        assert isinstance(call_part.args[0].value, ast.Call)
        assert isinstance(call_part.args[0].value.func, ast.Name) and call_part.args[0].value.func.id == "range"

def test_list_without_starred_no_change():
    source = "[1, 2, 3]"
    tree = parse_and_transform(source)
    # The AST should be unchanged except for generic_visit
    expr = tree.body[0].value
    assert isinstance(expr, ast.List)
    elts = expr.elts
    assert len(elts) == 3
    assert all(isinstance(e, ast.Num) and e.n in (1, 2, 3) for e in elts)
    # Ensure that the transformer did not set _tree_changed flag
    transformer = StarredUnpackingTransformer()
    transformer.visit(tree)
    assert not getattr(transformer, "_tree_changed", False)
