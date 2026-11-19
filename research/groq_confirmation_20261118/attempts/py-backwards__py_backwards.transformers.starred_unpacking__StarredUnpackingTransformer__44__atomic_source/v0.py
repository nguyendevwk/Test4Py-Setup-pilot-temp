import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer

def _parse_and_transform(code: str):
    """Parse the code with typed_ast, apply the transformer, and return the transformed AST."""
    tree = typed_ast.parse(code)
    transformer = StarredUnpackingTransformer()
    transformed = transformer.visit(tree)
    return transformed

def test_list_starred_unpacking():
    """Verify that a list with starred expressions is converted to a sum of lists."""
    code = "[2, *range(10), 1]"
    transformed = _parse_and_transform(code)
    # The top-level node should be a Module containing a Expr with a BinOp
    assert isinstance(transformed, typed_ast.Module)
    expr = transformed.body[0]
    assert isinstance(expr, typed_ast.Expr)
    binop = expr.value
    # The BinOp should be addition of three operands: [2], list(range(10)), [1]
    assert isinstance(binop, typed_ast.BinOp)
    assert isinstance(binop.op, typed_ast.Add)
    # Left operand should be a BinOp of [2] + list(range(10))
    left = binop.left
    assert isinstance(left, typed_ast.BinOp)
    assert isinstance(left.op, typed_ast.Add)
    assert isinstance(left.left, typed_ast.List)
    assert left.left.elts[0].n == 2
    assert isinstance(left.right, typed_ast.Call)
    assert isinstance(left.right.func, typed_ast.Name)
    assert left.right.func.id == "list"
    assert isinstance(left.right.args[0], typed_ast.Starred)
    # Right operand should be a List [1]
    right = binop.right
    assert isinstance(right, typed_ast.List)
    assert right.elts[0].n == 1

def test_call_starred_unpacking():
    """Verify that a function call with starred arguments is converted to a single starred list."""
    code = "print(*range(1), *range(3))"
    transformed = _parse_and_transform(code)
    # The top-level node should be a Module containing a Expr with a Call
    assert isinstance(transformed, typed_ast.Module)
    expr = transformed.body[0]
    assert isinstance(expr, typed_ast.Expr)
    call = expr.value
    assert isinstance(call, typed_ast.Call)
    # The call should have a single argument which is a Starred
    assert len(call.args) == 1
    starred = call.args[0]
    assert isinstance(starred, typed_ast.Starred)
    # The starred value should be a BinOp of two list(range(...)) calls
    binop = starred.value
    assert isinstance(binop, typed_ast.BinOp)
    assert isinstance(binop.op, typed_ast.Add)
    # Left operand: list(range(1))
    left = binop.left
    assert isinstance(left, typed_ast.Call)
    assert isinstance(left.func, typed_ast.Name)
    assert left.func.id == "list"
    assert isinstance(left.args[0], typed_ast.Starred)
    # Right operand: list(range(3))
    right = binop.right
    assert isinstance(right, typed_ast.Call)
    assert isinstance(right.func, typed_ast.Name)
    assert right.func.id == "list"
    assert isinstance(right.args[0], typed_ast.Starred)

def test_no_starred_no_change():
    """Verify that nodes without starred expressions are left unchanged."""
    code = "[1, 2, 3]"
    transformed = _parse_and_transform(code)
    # The transformed AST should be identical to the original
    original = typed_ast.parse(code)
    assert ast.dump(transformed) == ast.dump(original)
