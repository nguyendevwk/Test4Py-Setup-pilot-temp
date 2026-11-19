import ast
import typed_ast.ast3 as typed_ast
import pytest

from py_backwards.transformers.starred_unpacking import StarredUnpackingTransformer


def parse_and_transform(code: str) -> typed_ast.AST:
    """Parse the code with typed_ast and apply the transformer."""
    tree = typed_ast.parse(code)
    transformer = StarredUnpackingTransformer()
    transformer.visit(tree)
    return tree


def test_list_starred_unpacking():
    """Verify that a list with starred expressions is converted to a sum of lists."""
    code = "[2, *range(10), 1]"
    tree = parse_and_transform(code)

    # The top node should be a Module with a single Expr statement
    assert isinstance(tree, typed_ast.Module)
    expr = tree.body[0]
    assert isinstance(expr, typed_ast.Expr)

    # The value should be a BinOp representing the sum of lists
    binop = expr.value
    assert isinstance(binop, typed_ast.BinOp)
    assert isinstance(binop.op, typed_ast.Add)

    # Left side of the first addition should be a List with one element (2)
    left_list = binop.left
    assert isinstance(left_list, typed_ast.List)
    assert len(left_list.elts) == 1
    assert isinstance(left_list.elts[0], typed_ast.Num)
    assert left_list.elts[0].n == 2

    # Right side should be another BinOp (the second addition)
    right_binop = binop.right
    assert isinstance(right_binop, typed_ast.BinOp)
    assert isinstance(right_binop.op, typed_ast.Add)

    # The left side of the second addition should be a Call to list(range(10))
    call = right_binop.left
    assert isinstance(call, typed_ast.Call)
    assert isinstance(call.func, typed_ast.Name)
    assert call.func.id == "list"
    assert len(call.args) == 1
    assert isinstance(call.args[0], typed_ast.Call)
    assert isinstance(call.args[0].func, typed_ast.Name)
    assert call.args[0].func.id == "range"

    # The right side of the second addition should be a List with one element (1)
    right_list = right_binop.right
    assert isinstance(right_list, typed_ast.List)
    assert len(right_list.elts) == 1
    assert isinstance(right_list.elts[0], typed_ast.Num)
    assert right_list.elts[0].n == 1


def test_call_starred_unpacking():
    """Verify that a call with starred arguments is converted to a single starred argument."""
    code = "print(*range(1), *range(3))"
    tree = parse_and_transform(code)

    # The top node should be a Module with a single Expr statement
    assert isinstance(tree, typed_ast.Module)
    expr = tree.body[0]
    assert isinstance(expr, typed_ast.Expr)

    # The value should be a Call to print
    call = expr.value
    assert isinstance(call, typed_ast.Call)
    assert isinstance(call.func, typed_ast.Name)
    assert call.func.id == "print"

    # The call should have exactly one argument, which is a Starred
    assert len(call.args) == 1
    starred = call.args[0]
    assert isinstance(starred, typed_ast.Starred)

    # The value of the starred should be a BinOp representing the sum of lists
    binop = starred.value
    assert isinstance(binop, typed_ast.BinOp)
    assert isinstance(binop.op, typed_ast.Add)

    # The left side of the BinOp should be a Call to list(range(1))
    left_call = binop.left
    assert isinstance(left_call, typed_ast.Call)
    assert isinstance(left_call.func, typed_ast.Name)
    assert left_call.func.id == "list"
    assert len(left_call.args) == 1
    assert isinstance(left_call.args[0], typed_ast.Call)
    assert isinstance(left_call.args[0].func, typed_ast.Name)
    assert left_call.args[0].func.id == "range"

    # The right side of the BinOp should be a Call to list(range(3))
    right_call = binop.right
    assert isinstance(right_call, typed_ast.Call)
    assert isinstance(right_call.func, typed_ast.Name)
    assert right_call.func.id == "list"
    assert len(right_call.args) == 1
    assert isinstance(right_call.args[0], typed_ast.Call)
    assert isinstance(right_call.args[0].func, typed_ast.Name)
    assert right_call.args[0].func.id == "range"


def test_no_starred_no_change():
    """Ensure that nodes without starred expressions are left unchanged."""
    code = "[1, 2, 3]"
    tree = parse_and_transform(code)

    # The top node should be a Module with a single Expr statement
    assert isinstance(tree, typed_ast.Module)
    expr = tree.body[0]
    assert isinstance(expr, typed_ast.Expr)

    # The value should be a List with three elements
    lst = expr.value
    assert isinstance(lst, typed_ast.List)
    assert len(lst.elts) == 3
    for i, el in enumerate(lst.elts, start=1):
        assert isinstance(el, typed_ast.Num)
        assert el.n == i
