import ast
import pytest
from apimd.parser import walk_body

def test_walk_body_simple_sequence():
    # Parse a simple function body with an if and a try
    source = """
def foo():
    if True:
        x = 1
    else:
        x = 2
    try:
        y = 3
    except Exception:
        y = 4
    finally:
        z = 5
"""
    module = ast.parse(source)
    # Extract the function body
    func = next(node for node in module.body if isinstance(node, ast.FunctionDef))
    body = func.body

    # Collect the nodes yielded by walk_body
    yielded = list(walk_body(body))

    # The order should be: If node, its body nodes, its orelse nodes,
    # Try node, its body nodes, handler body nodes, finally body nodes
    # We check that the first node is the If statement
    assert isinstance(yielded[0], ast.If)
    # The second node should be the Assign inside the if body
    assert isinstance(yielded[1], ast.Assign)
    # The third node should be the Assign inside the else body
    assert isinstance(yielded[2], ast.Assign)
    # The fourth node should be the Try statement
    assert isinstance(yielded[3], ast.Try)
    # The fifth node should be the Assign inside the try body
    assert isinstance(yielded[4], ast.Assign)
    # The sixth node should be the Assign inside the except handler
    assert isinstance(yielded[5], ast.Assign)
    # The seventh node should be the Assign inside the finally body
    assert isinstance(yielded[6], ast.Assign)

def test_walk_body_empty_sequence():
    # An empty body should yield nothing
    empty_body = []
    result = list(walk_body(empty_body))
    assert result == []

def test_walk_body_invalid_input():
    # Passing a non-sequence should raise a TypeError when iterated
    with pytest.raises(TypeError):
        list(walk_body(42))
