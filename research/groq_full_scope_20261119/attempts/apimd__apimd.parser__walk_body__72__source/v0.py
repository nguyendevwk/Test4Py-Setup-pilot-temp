import ast
import pytest
from apimd.parser import walk_body

def test_walk_body_traverses_nested_if_and_try():
    source = """
def foo():
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
    body = module.body[0].body  # body of function foo
    nodes = list(walk_body(body))
    # Expected order: a, b, c, d, e
    names = [node.targets[0].id if isinstance(node, ast.Assign) else None for node in nodes]
    assert names == ["a", "b", "c", "d", "e"]

def test_walk_body_empty_body_returns_no_nodes():
    empty_body = []
    assert list(walk_body(empty_body)) == []

def test_walk_body_yields_all_non_control_nodes_in_order():
    source = """
x = 1
if False:
    y = 2
z = 3
"""
    module = ast.parse(source)
    body = module.body
    nodes = list(walk_body(body))
    # Should yield the two assignments in order, skipping the if block
    assert len(nodes) == 2
    assert isinstance(nodes[0], ast.Assign)
    assert isinstance(nodes[1], ast.Assign)
    assert nodes[0].targets[0].id == "x"
    assert nodes[1].targets[0].id == "z"
