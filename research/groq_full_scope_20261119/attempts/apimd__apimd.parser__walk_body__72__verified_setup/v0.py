import ast
import pytest
from apimd.parser import walk_body

def test_walk_body_empty_sequence():
    """walk_body should yield nothing for an empty body."""
    body = []
    result = list(walk_body(body))
    assert result == [], "Expected no nodes to be yielded for an empty body"

def test_walk_body_nested_if_and_try():
    """walk_body should correctly traverse nested If and Try structures."""
    source = """
if True:
    a = 1
else:
    b = 2
try:
    c = 3
except Exception:
    d = 4
finally:
    e = 5
"""
    module = ast.parse(source)
    body = module.body
    nodes = list(walk_body(body))
    # Extract node types in order
    types = [type(node).__name__ for node in nodes]
    expected = [
        "Assign",  # a = 1
        "Assign",  # b = 2
        "Assign",  # c = 3
        "Assign",  # d = 4
        "Assign",  # e = 5
    ]
    assert types == expected, f"Expected node types {expected}, got {types}"

def test_walk_body_invalid_input_type():
    """walk_body should raise a TypeError when body is not a sequence of stmts."""
    with pytest.raises(TypeError):
        # Pass an integer which is not iterable
        list(walk_body(42))
