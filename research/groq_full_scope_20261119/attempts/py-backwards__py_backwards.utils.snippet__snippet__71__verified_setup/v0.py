import ast
import inspect
import types
import pytest
from py_backwards.utils.snippet import snippet

def test_snippet_basic_body_extraction(tmp_path):
    # Define a simple function that uses a local variable
    def foo():
        x = 1
        return x + 2

    # Create a snippet from the function
    snip = snippet(foo)

    # Get the AST body of the snippet
    body = snip.get_body()

    # The body should be a list of AST nodes
    assert isinstance(body, list)
    # The first node should be an Assign node for `x = 1`
    assert isinstance(body[0], ast.Assign)
    # The target of the assignment should be a Name node with id 'x'
    assert isinstance(body[0].targets[0], ast.Name)
    assert body[0].targets[0].id == 'x'
    # The value should be a Constant node with value 1
    assert isinstance(body[0].value, ast.Constant)
    assert body[0].value.value == 1

def test_snippet_variable_override(tmp_path):
    # Function that references a variable `y`
    def bar():
        return y * 3

    snip = snippet(bar)

    # Override `y` with a literal value
    body = snip.get_body(y=5)

    # The body should contain a Return node
    assert isinstance(body[0], ast.Return)
    # The value of the return should be a BinOp
    assert isinstance(body[0].value, ast.BinOp)
    # The left operand should be a Constant with value 5
    left = body[0].value.left
    assert isinstance(left, ast.Constant)
    assert left.value == 5
    # The right operand should be a Constant with value 3
    right = body[0].value.right
    assert isinstance(right, ast.Constant)
    assert right.value == 3

def test_snippet_invalid_override_type(tmp_path):
    # Function that uses variable `z`
    def baz():
        return z + 1

    snip = snippet(baz)

    # Passing an unsupported type (e.g., a list) should raise a TypeError
    with pytest.raises(TypeError):
        snip.get_body(z=[1, 2, 3])
