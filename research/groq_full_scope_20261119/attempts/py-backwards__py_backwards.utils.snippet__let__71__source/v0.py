import ast
import pytest
from py_backwards.utils.snippet import let, get_source
from typed_ast import ast3 as typed_ast

def test_simple_let_and_usage(tmp_path):
    # Create a simple snippet that declares a variable and uses it
    code = """
let(x)
x += 1
y = 1
"""
    # Parse the code into an AST
    tree = typed_ast.parse(code)
    # Apply the let transformation
    let(tree)
    # Convert the transformed AST back to source code
    transformed = get_source(tree)
    # The variable `x` should be renamed to a unique name
    assert "_py_backwards_x_" in transformed
    # The assignment to y should remain unchanged
    assert "y = 1" in transformed
    # The increment should reference the renamed variable
    assert transformed.count("_py_backwards_x_") == 1
    assert "+= 1" in transformed

def test_multiple_lets_and_unique_names(tmp_path):
    # Declare the same variable twice and use it
    code = """
let(x)
x += 1
let(x)
x += 2
"""
    tree = typed_ast.parse(code)
    let(tree)
    transformed = get_source(tree)
    # Two unique names should appear for the two let declarations
    names = [n for n in transformed.splitlines() if "_py_backwards_x_" in n]
    assert len(names) == 2
    # The increments should refer to the correct unique names
    assert "_py_backwards_x_0 += 1" in transformed
    assert "_py_backwards_x_1 += 2" in transformed

def test_let_on_expression_raises_error(tmp_path):
    # Attempt to use let on an expression (should raise an error)
    code = """
let(1)
"""
    tree = typed_ast.parse(code)
    with pytest.raises(TypeError):
        let(tree)
