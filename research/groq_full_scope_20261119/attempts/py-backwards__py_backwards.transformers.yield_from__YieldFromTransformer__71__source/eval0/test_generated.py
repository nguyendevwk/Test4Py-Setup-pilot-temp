import ast
import pytest
from py_backwards.transformers.yield_from import YieldFromTransformer
from typed_ast import ast3 as typed_ast

def has_yield_from(node):
    """Return True if the AST contains any ast.YieldFrom nodes."""
    return any(isinstance(n, typed_ast.YieldFrom) for n in typed_ast.walk(node))

def test_assignment_yield_from_replaced(tmp_path):
    source = """
def f():
    x = yield from iterable
    return x
"""
    tree = typed_ast.parse(source)
    transformer = YieldFromTransformer()
    new_tree = transformer.visit(tree)
    # The transformed tree should no longer contain any YieldFrom nodes
    assert not has_yield_from(new_tree)
    # The assignment target 'x' should still be present
    assigns = [n for n in typed_ast.walk(new_tree) if isinstance(n, typed_ast.Assign)]
    assert len(assigns) == 1
    assert isinstance(assigns[0].targets[0], typed_ast.Name)
    assert assigns[0].targets[0].id == 'x'

def test_expression_yield_from_replaced(tmp_path):
    source = """
def g():
    yield from iterable
"""
    tree = typed_ast.parse(source)
    transformer = YieldFromTransformer()
    new_tree = transformer.visit(tree)
    # No YieldFrom nodes should remain
    assert not has_yield_from(new_tree)
    # The function body should contain a statement that is not an Expr
    # (the yield_from transformation replaces the Expr with a while loop)
    stmts = list(typed_ast.iter_child_nodes(new_tree.body[0]))
    assert len(stmts) == 1
    assert isinstance(stmts[0], typed_ast.While)

def test_no_yield_from_unchanged(tmp_path):
    source = """
def h():
    a = 1
    b = 2
    return a + b
"""
    tree = typed_ast.parse(source)
    transformer = YieldFromTransformer()
    new_tree = transformer.visit(tree)
    # The tree should be identical to the original (no changes)
    assert typed_ast.dump(tree) == typed_ast.dump(new_tree)
    # Ensure no YieldFrom nodes are present
    assert not has_yield_from(new_tree)
