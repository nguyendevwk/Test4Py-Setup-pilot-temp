import ast
import inspect
import types
import pytest

from py_backwards.utils.snippet import snippet
from py_backwards.utils.helpers import get_source
from py_backwards.utils.tree import find, get_non_exp_parent_and_index, replace_at


def test_snippet_replaces_variables_correctly():
    # Define a simple function that uses a variable placeholder
    def func():
        x = 1
        y = 2
        return x + y

    # Wrap the function in a snippet
    snip = snippet(func)

    # Call get_body with a custom value for 'x'
    body = snip.get_body(x=10)

    # The body should be a list of AST nodes; the first should be an Assign to y
    assert isinstance(body, list)
    assert len(body) == 2

    # The first node should be the assignment to y
    assign_y = body[0]
    assert isinstance(assign_y, ast.Assign)
    assert isinstance(assign_y.targets[0], ast.Name)
    assert assign_y.targets[0].id == "y"
    assert isinstance(assign_y.value, ast.Constant)
    assert assign_y.value.value == 2

    # The second node should be the return statement
    ret = body[1]
    assert isinstance(ret, ast.Return)
    # The return value should be a BinOp with left operand 10 (our replacement for x)
    assert isinstance(ret.value, ast.BinOp)
    assert isinstance(ret.value.left, ast.Constant)
    assert ret.value.left.value == 10
    assert isinstance(ret.value.right, ast.Name)
    assert ret.value.right.id == "y"


def test_snippet_accepts_ast_name_as_variable():
    # Function that uses a variable placeholder
    def func():
        return a + b

    snip = snippet(func)

    # Pass an ast.Name instance for 'a'
    name_a = ast.Name(id="alpha", ctx=ast.Load())
    body = snip.get_body(a=name_a)

    # The return statement should use 'alpha' instead of 'a'
    ret = body[0]
    assert isinstance(ret, ast.Return)
    assert isinstance(ret.value, ast.BinOp)
    assert isinstance(ret.value.left, ast.Name)
    assert ret.value.left.id == "alpha"
    assert isinstance(ret.value.right, ast.Name)
    assert ret.value.right.id == "b"


def test_snippet_raises_on_missing_variable():
    # Function that references a variable not provided
    def func():
        return x + 1

    snip = snippet(func)

    # Calling get_body without providing 'x' should raise a KeyError
    with pytest.raises(KeyError):
        snip.get_body()
