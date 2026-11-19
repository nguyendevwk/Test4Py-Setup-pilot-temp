import ast
import pytest
from py_backwards.utils.snippet import snippet, Variable, VariablesGenerator, get_source, find, get_non_exp_parent_and_index, replace_at, extend_tree, find_variables, VariablesReplacer


def test_snippet_basic_variable_replacement(tmp_path):
    # Define a simple function with a let and extend call
    def f():
        let(x)
        extend(x)
        return x + 1

    # Create snippet and get body
    snip = snippet(f)
    body = snip.get_body()

    # The body should contain a return statement
    assert len(body) == 1
    assert isinstance(body[0], ast.Return)

    # The returned expression should be a BinOp with the variable replaced
    expr = body[0].value
    assert isinstance(expr, ast.BinOp)
    assert isinstance(expr.left, ast.Name)
    assert expr.left.id != "x"  # variable should be replaced
    # The generated name should be unique and start with _var_
    assert expr.left.id.startswith("_var_")
    # The right side should be the constant 1
    assert isinstance(expr.right, ast.Constant) and expr.right.value == 1


def test_snippet_with_explicit_kwargs(tmp_path):
    # Function that uses a variable that will be overridden by kwargs
    def g():
        let(y)
        extend(y)
        return y * 2

    snip = snippet(g)
    # Override y with a literal value
    body = snip.get_body(y=5)

    # The body should contain a return statement
    assert len(body) == 1
    assert isinstance(body[0], ast.Return)

    # The returned expression should be a BinOp with the literal 5
    expr = body[0].value
    assert isinstance(expr, ast.BinOp)
    assert isinstance(expr.left, ast.Constant) and expr.left.value == 5
    assert isinstance(expr.right, ast.Constant) and expr.right.value == 2


def test_snippet_error_on_invalid_call(tmp_path):
    # Function that contains a let call with a non-name argument
    def h():
        let(1)  # invalid: argument is not a Name node
        return 0

    snip = snippet(h)
    # get_body should raise a TypeError because find_variables expects a Name
    with pytest.raises(TypeError):
        snip.get_body()
