import ast
import pytest
from apimd.parser import walk_body

def test_walk_body_simple_if():
    """walk_body should traverse nodes inside an If statement."""
    source = """
if True:
    a = 1
else:
    b = 2
c = 3
"""
    module = ast.parse(source)
    body = module.body
    nodes = list(walk_body(body))
    # Expect the assignment nodes in order: a=1, b=2, c=3
    assert len(nodes) == 3
    assert isinstance(nodes[0], ast.Assign)
    assert isinstance(nodes[1], ast.Assign)
    assert isinstance(nodes[2], ast.Assign)
    # Check that the targets are correct
    assert nodes[0].targets[0].id == "a"
    assert nodes[1].targets[0].id == "b"
    assert nodes[2].targets[0].id == "c"

def test_walk_body_empty_body():
    """walk_body should handle an empty body without errors."""
    body: list[ast.stmt] = []
    nodes = list(walk_body(body))
    assert nodes == []

def test_walk_body_invalid_input():
    """walk_body should raise a TypeError when given a non-iterable."""
    with pytest.raises(TypeError):
        list(walk_body(42))
