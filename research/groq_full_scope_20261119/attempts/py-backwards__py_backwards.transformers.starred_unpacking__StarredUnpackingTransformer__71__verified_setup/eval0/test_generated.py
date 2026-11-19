import pytest
from typed_ast import ast3 as ast
from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer


def _transform(source: str) -> ast.AST:
    """Parse source, apply transformer, and return the transformed AST."""
    tree = ast.parse(source)
    transformer = StarredUnpackingTransformer()
    transformer.visit(tree)
    return tree


def test_list_with_starred_unpacking():
    """A list containing a starred expression should be transformed into a BinOp of lists."""
    source = "[2, *range(10), 1]"
    tree = _transform(source)

    # The top-level node should be a Module with a single Expr statement.
    assert isinstance(tree, ast.Module)
    expr = tree.body[0]
    assert isinstance(expr, ast.Expr)

    # The value of the Expr should be a BinOp (2 + list(range(10)) + 1).
    binop = expr.value
    assert isinstance(binop, ast.BinOp)
    assert isinstance(binop.op, ast.Add)

    # Left side of the outer BinOp should itself be a BinOp (2 + list(range(10))).
    left_binop = binop.left
    assert isinstance(left_binop, ast.BinOp)
    assert isinstance(left_binop.op, ast.Add)

    # The leftmost operand should be a List with a single element 2.
    left_list = left_binop.left
    assert isinstance(left_list, ast.List)
    assert len(left_list.elts) == 1
    assert isinstance(left_list.elts[0], ast.Num) and left_list.elts[0].n == 2

    # The middle operand should be a Call to list(range(10)).
    middle_call = left_binop.right
    assert isinstance(middle_call, ast.Call)
    assert isinstance(middle_call.func, ast.Name) and middle_call.func.id == "list"
    assert isinstance(middle_call.args[0], ast.Call)
    assert isinstance(middle_call.args[0].func, ast.Name) and middle_call.args[0].func.id == "range"
    assert isinstance(middle_call.args[0].args[0], ast.Num) and middle_call.args[0].args[0].n == 10

    # The rightmost operand of the outer BinOp should be a List with a single element 1.
    right_list = binop.right
    assert isinstance(right_list, ast.List)
    assert len(right_list.elts) == 1
    assert isinstance(right_list.elts[0], ast.Num) and right_list.elts[0].n == 1


def test_call_with_starred_unpacking():
    """A function call with starred arguments should be transformed into a single starred argument
    that is a sum of lists."""
    source = "print(*range(1), *range(3))"
    tree = _transform(source)

    # The top-level node should be a Module with a single Expr statement.
    assert isinstance(tree, ast.Module)
    expr = tree.body[0]
    assert isinstance(expr, ast.Expr)

    # The value of the Expr should be a Call to print.
    call = expr.value
    assert isinstance(call, ast.Call)
    assert isinstance(call.func, ast.Name) and call.func.id == "print"

    # After transformation, there should be exactly one argument: a starred expression.
    assert len(call.args) == 1
    starred = call.args[0]
    assert isinstance(starred, ast.Starred)

    # The starred value should be a BinOp representing list(range(1)) + list(range(3)).
    binop = starred.value
    assert isinstance(binop, ast.BinOp)
    assert isinstance(binop.op, ast.Add)

    # Left operand: list(range(1))
    left_call = binop.left
    assert isinstance(left_call, ast.Call)
    assert isinstance(left_call.func, ast.Name) and left_call.func.id == "list"
    assert isinstance(left_call.args[0], ast.Call)
    assert isinstance(left_call.args[0].func, ast.Name) and left_call.args[0].func.id == "range"
    assert isinstance(left_call.args[0].args[0], ast.Num) and left_call.args[0].args[0].n == 1

    # Right operand: list(range(3))
    right_call = binop.right
    assert isinstance(right_call, ast.Call)
    assert isinstance(right_call.func, ast.Name) and right_call.func.id == "list"
    assert isinstance(right_call.args[0], ast.Call)
    assert isinstance(right_call.args[0].func, ast.Name) and right_call.args[0].func.id == "range"
    assert isinstance(right_call.args[0].args[0], ast.Num) and right_call.args[0].args[0].n == 3


def test_no_starred_no_change():
    """A list or call without starred expressions should remain unchanged."""
    source = "[1, 2, 3]"
    tree = _transform(source)

    # The structure should be identical to the original AST.
    assert isinstance(tree, ast.Module)
    expr = tree.body[0]
    assert isinstance(expr, ast.Expr)
    assert isinstance(expr.value, ast.List)
    elts = expr.value.elts
    assert len(elts) == 3
    assert all(isinstance(e, ast.Num) for e in elts)
    assert [e.n for e in elts] == [1, 2, 3]
