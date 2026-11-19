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


def test_starred_in_list_transforms_to_binop():
    """A list containing a starred expression should be converted to a BinOp of lists."""
    code = "[2, *range(10), 1]"
    tree = _parse_and_transform(code)

    # The top-level node is a Module with a single Expr
    expr = tree.body[0]
    assert isinstance(expr, ast.Expr)

    # The value should be a BinOp (2 + list(range(10)) + 1)
    binop = expr.value
    assert isinstance(binop, ast.BinOp)

    # Left side of the outer BinOp should itself be a BinOp
    left_binop = binop.left
    assert isinstance(left_binop, ast.BinOp)

    # The leftmost operand should be a List with one element 2
    left_list = left_binop.left
    assert isinstance(left_list, ast.List)
    assert len(left_list.elts) == 1
    assert isinstance(left_list.elts[0], ast.Num) and left_list.elts[0].n == 2

    # The middle operand should be a Call to list(range(10))
    middle_call = left_binop.right
    assert isinstance(middle_call, ast.Call)
    assert isinstance(middle_call.func, ast.Name) and middle_call.func.id == "list"
    assert isinstance(middle_call.args[0], ast.Call)
    assert isinstance(middle_call.args[0].func, ast.Name) and middle_call.args[0].func.id == "range"

    # The rightmost operand should be a List with one element 1
    right_list = binop.right
    assert isinstance(right_list, ast.List)
    assert len(right_list.elts) == 1
    assert isinstance(right_list.elts[0], ast.Num) and right_list.elts[0].n == 1


def test_starred_in_call_transforms_to_single_starred_sum():
    """A function call with starred arguments should wrap the sum of lists in a single starred argument."""
    code = "print(*range(1), *range(3))"
    tree = _parse_and_transform(code)

    # The top-level node is a Module with a single Expr
    expr = tree.body[0]
    assert isinstance(expr, ast.Expr)

    # The value should be a Call to print
    call = expr.value
    assert isinstance(call, ast.Call)
    assert isinstance(call.func, ast.Name) and call.func.id == "print"

    # There should be exactly one argument, which is a Starred
    assert len(call.args) == 1
    starred = call.args[0]
    assert isinstance(starred, ast.Starred)

    # The starred value should be a BinOp representing list(range(1)) + list(range(3))
    binop = starred.value
    assert isinstance(binop, ast.BinOp)

    # Left operand: list(range(1))
    left_call = binop.left
    assert isinstance(left_call, ast.Call)
    assert isinstance(left_call.func, ast.Name) and left_call.func.id == "list"
    assert isinstance(left_call.args[0], ast.Call)
    assert isinstance(left_call.args[0].func, ast.Name) and left_call.args[0].func.id == "range"

    # Right operand: list(range(3))
    right_call = binop.right
    assert isinstance(right_call, ast.Call)
    assert isinstance(right_call.func, ast.Name) and right_call.func.id == "list"
    assert isinstance(right_call.args[0], ast.Call)
    assert isinstance(right_call.args[0].func, ast.Name) and right_call.args[0].func.id == "range"


def test_no_starred_unchanged():
    """A list or call without starred expressions should remain unchanged."""
    code = "[1, 2, 3]"
    tree = _parse_and_transform(code)

    # The top-level node is a Module with a single Expr
    expr = tree.body[0]
    assert isinstance(expr, ast.Expr)

    # The value should still be a List with three elements
    lst = expr.value
    assert isinstance(lst, ast.List)
    assert len(lst.elts) == 3
    assert all(isinstance(e, ast.Num) for e in lst.elts)
    assert [e.n for e in lst.elts] == [1, 2, 3]
