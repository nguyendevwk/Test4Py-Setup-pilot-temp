import ast
import inspect
import types
import pytest
from py_backwards.utils.snippet import snippet
from typed_ast import ast3 as typed_ast

def test_snippet_basic_returns_constant():
    # A simple function that returns a constant
    def f():
        return 42

    snip = snippet(f)
    body = snip.get_body()
    # body should contain a single Return node
    assert len(body) == 1
    node = body[0]
    assert isinstance(node, typed_ast.Return)
    assert isinstance(node.value, typed_ast.Constant)
    assert node.value.value == 42

def test_snippet_variable_replacement_with_value():
    # Function that uses a variable in its return expression
    def g():
        return x + 1

    snip = snippet(g)
    # Replace variable `x` with a concrete value
    body = snip.get_body(x=10)
    # The body should contain a Return node with a BinOp
    node = body[0]
    assert isinstance(node, typed_ast.Return)
    assert isinstance(node.value, typed_ast.BinOp)
    # The left side of the BinOp should be the constant 10
    left = node.value.left
    assert isinstance(left, typed_ast.Constant)
    assert left.value == 10
    # The right side should be the constant 1
    right = node.value.right
    assert isinstance(right, typed_ast.Constant)
    assert right.value == 1

def test_snippet_variable_replacement_with_ast_name():
    # Function that uses a variable in its return expression
    def h():
        return y * 2

    snip = snippet(h)
    # Replace variable `y` with an AST Name node
    body = snip.get_body(y=typed_ast.Name(id='z', ctx=typed_ast.Load()))
    node = body[0]
    assert isinstance(node, typed_ast.Return)
    assert isinstance(node.value, typed_ast.BinOp)
    # The left side should now be a Name node with id 'z'
    left = node.value.left
    assert isinstance(left, typed_ast.Name)
    assert left.id == 'z'
    # The right side should be the constant 2
    right = node.value.right
    assert isinstance(right, typed_ast.Constant)
    assert right.value == 2
