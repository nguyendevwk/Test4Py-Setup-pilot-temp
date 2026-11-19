import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer

def _transform(source: str) -> ast.AST:
    """Parse source with typed_ast, apply transformer, and return the transformed AST."""
    tree = typed_ast.parse(source)
    transformer = StarredUnpackingTransformer()
    return transformer.visit(tree)

def _unparse(node: ast.AST) -> str:
    """Unparse a typed_ast node using the standard ast.unparse if available."""
    return ast.unparse(node)

def test_list_with_starred_unpacking():
    source = "[2, *range(10), 1]"
    transformed = _transform(source)
    # The top-level node should be a Module with a single Expr containing a BinOp
    assert isinstance(transformed, typed_ast.Module)
    expr = transformed.body[0]
    assert isinstance(expr, typed_ast.Expr)
    binop = expr.value
    assert isinstance(binop, typed_ast.BinOp)
    # The left side should be a BinOp (2 + list(range(10)))
    left = binop.left
    assert isinstance(left, typed_ast.BinOp)
    assert isinstance(left.left, typed_ast.List)
    assert isinstance(left.right, typed_ast.Call)
    # The right side should be a List containing 1
    right = binop.right
    assert isinstance(right, typed_ast.List)
    assert len(right.elts) == 1
    assert isinstance(right.elts[0], typed_ast.Constant) and right.elts[0].value == 1

def test_call_with_multiple_starred_args():
    source = "print(*range(1), *range(3))"
    transformed = _transform(source)
    # The top-level node should be a Module with a single Expr containing a Call
    assert isinstance(transformed, typed_ast.Module)
    expr = transformed.body[0]
    assert isinstance(expr, typed_ast.Expr)
    call = expr.value
    assert isinstance(call, typed_ast.Call)
    # The call should have a single starred argument that is a BinOp
    assert len(call.args) == 1
    starred = call.args[0]
    assert isinstance(starred, typed_ast.Starred)
    binop = starred.value
    assert isinstance(binop, typed_ast.BinOp)
    # The left side of the BinOp should be list(range(1))
    left = binop.left
    assert isinstance(left, typed_ast.Call)
    assert isinstance(left.func, typed_ast.Name) and left.func.id == "list"
    # The right side should be list(range(3))
    right = binop.right
    assert isinstance(right, typed_ast.Call)
    assert isinstance(right.func, typed_ast.Name) and right.func.id == "list"

def test_no_starred_unchanged():
    source = "[1, 2, 3]"
    transformed = _transform(source)
    # The transformed AST should be identical to the original
    original = typed_ast.parse(source)
    assert ast.dump(transformed) == ast.dump(original)
