import ast
import pytest
from apimd.parser import walk_body

def test_walk_body_simple_sequence():
    # A simple body with two statements: assignment and expression
    body = ast.parse("x = 1\nprint(x)").body
    # Convert generator to list
    nodes = list(walk_body(body))
    # Expect exactly two nodes in order
    assert len(nodes) == 2
    assert isinstance(nodes[0], ast.Assign)
    assert isinstance(nodes[1], ast.Expr)
    # The assignment should assign to 'x'
    assert isinstance(nodes[0].targets[0], ast.Name)
    assert nodes[0].targets[0].id == "x"
    # The expression should be a call to print
    assert isinstance(nodes[1].value, ast.Call)
    assert isinstance(nodes[1].value.func, ast.Name)
    assert nodes[1].value.func.id == "print"

def test_walk_body_nested_if_and_try():
    # Build a body with nested If and Try structures
    code = """
if True:
    a = 1
else:
    a = 2
try:
    b = a + 1
except Exception:
    b = 0
finally:
    c = b * 2
"""
    body = ast.parse(code).body
    nodes = list(walk_body(body))
    # The walk_body should yield all statements in the order they appear
    # after flattening the If and Try blocks.
    # Expected sequence: a=1, a=2, b=a+1, b=0, c=b*2
    assert len(nodes) == 5
    # Check types and order
    assert isinstance(nodes[0], ast.Assign) and nodes[0].targets[0].id == "a"
    assert isinstance(nodes[1], ast.Assign) and nodes[1].targets[0].id == "a"
    assert isinstance(nodes[2], ast.Assign) and nodes[2].targets[0].id == "b"
    assert isinstance(nodes[3], ast.Assign) and nodes[3].targets[0].id == "b"
    assert isinstance(nodes[4], ast.Assign) and nodes[4].targets[0].id == "c"

def test_walk_body_invalid_input_raises_type_error():
    # walk_body expects an iterable of stmt nodes; passing a non-iterable should raise TypeError
    with pytest.raises(TypeError):
        list(walk_body(42))
