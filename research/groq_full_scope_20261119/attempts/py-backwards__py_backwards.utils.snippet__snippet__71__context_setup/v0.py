import ast
import inspect
import pytest
from py_backwards.utils.snippet import snippet, VariablesGenerator, get_source

def test_snippet_replaces_variables_and_extends():
    # Define a function that uses `let` and `extend`
    def f():
        let = lambda x: x  # placeholder, will be removed
        extend = lambda x: x  # placeholder, will be replaced
        let(a)
        extend(a)
        return a + 1

    # Create snippet and get body AST
    snip = snippet(f)
    body = snip.get_body(a=5)

    # The body should contain a single return statement with value 5 + 1
    assert len(body) == 1
    assert isinstance(body[0], ast.Return)
    assert ast.unparse(body[0].value).strip() == "5 + 1"

def test_snippet_without_let_calls_returns_original_body():
    # Function with no `let` calls; snippet should return the body unchanged
    def g():
        x = 10
        return x * 2

    snip = snippet(g)
    body = snip.get_body()
    # Body should contain the assignment and return
    assert len(body) == 2
    assert isinstance(body[0], ast.Assign)
    assert isinstance(body[1], ast.Return)
    assert ast.unparse(body[1].value).strip() == "x * 2"

def test_snippet_with_invalid_variable_type_raises():
    # Function that uses a variable that will be replaced by a non-ast node
    def h():
        let = lambda x: x
        let(y)
        return y

    snip = snippet(h)
    # Passing a string as variable value should be accepted, but
    # passing an unsupported type (e.g., a list) should raise a TypeError
    with pytest.raises(TypeError):
        snip.get_body(y=[1, 2, 3])
