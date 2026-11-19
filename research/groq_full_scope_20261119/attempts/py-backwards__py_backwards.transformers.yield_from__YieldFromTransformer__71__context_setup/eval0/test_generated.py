import pytest
import typed_ast.ast3 as ast
from py_backwards.transformers.yield_from import YieldFromTransformer


def test_get_yield_from_index_finds_assignment():
    """_get_yield_from_index should return the index of an Assign node
    whose value is a YieldFrom, and None otherwise."""
    transformer = YieldFromTransformer()
    # Build a dummy node with a body containing an Assign with YieldFrom
    assign_node = ast.Assign(
        targets=[ast.Name(id='x', ctx=ast.Store())],
        value=ast.YieldFrom(value=ast.Name(id='iterable', ctx=ast.Load()))
    )
    dummy = ast.Module(body=[assign_node], type_ignores=[])
    index = transformer._get_yield_from_index(dummy, ast.Assign)
    assert index == 0, "Index should point to the first (and only) Assign node"

    # Test when no matching node exists
    dummy.body = [ast.Expr(value=ast.Name(id='y', ctx=ast.Load()))]
    index = transformer._get_yield_from_index(dummy, ast.Assign)
    assert index is None, "Should return None when no matching Assign node"


def test_handle_assignments_replaces_yield_from_with_while():
    """After visiting a module containing an assignment with yield from,
    the assignment should be replaced by a while loop and no YieldFrom nodes
    should remain."""
    code = """
def foo():
    a = (yield from iterable)
"""
    tree = ast.parse(code)
    transformer = YieldFromTransformer()
    transformed = transformer.visit(tree)

    # The transformed body should contain a While node instead of Assign
    assert any(isinstance(node, ast.While) for node in transformed.body[0].body), \
        "Expected a While node to replace the assignment"

    # No Assign or YieldFrom nodes should remain
    for node in ast.walk(transformed):
        assert not isinstance(node, ast.Assign), "Assign node should have been removed"
        assert not isinstance(node, ast.YieldFrom), "YieldFrom node should have been removed"


def test_handle_expressions_replaces_yield_from_with_while():
    """After visiting a module containing an expression with yield from,
    the expression should be replaced by a while loop and no YieldFrom nodes
    should remain."""
    code = """
def bar():
    (yield from iterable)
"""
    tree = ast.parse(code)
    transformer = YieldFromTransformer()
    transformed = transformer.visit(tree)

    # The transformed body should contain a While node instead of Expr
    assert any(isinstance(node, ast.While) for node in transformed.body[0].body), \
        "Expected a While node to replace the expression"

    # No Expr or YieldFrom nodes should remain
    for node in ast.walk(transformed):
        assert not isinstance(node, ast.Expr), "Expr node should have been removed"
        assert not isinstance(node, ast.YieldFrom), "YieldFrom node should have been removed"
