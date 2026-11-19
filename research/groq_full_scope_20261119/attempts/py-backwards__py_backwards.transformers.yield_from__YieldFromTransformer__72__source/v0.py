import ast
import typed_ast.ast3 as ast3
import pytest
from py_backwards.transformers.yield_from import YieldFromTransformer

def make_module(source: str) -> ast3.Module:
    """Parse source into a typed_ast3 Module."""
    return ast3.parse(source, mode="exec")

def ast_to_source(node: ast3.AST) -> str:
    """Convert an AST back to source code for easier inspection."""
    return ast.unparse(node)

def test_assignment_yield_from_replaced():
    src = """
def f():
    a = yield from range(3)
"""
    mod = make_module(src)
    transformer = YieldFromTransformer()
    transformed = transformer.visit(mod)
    # Ensure no YieldFrom nodes remain
    for node in ast3.walk(transformed):
        assert not isinstance(node, ast3.YieldFrom)
    # The assignment target 'a' should still be present
    assigns = [n for n in ast3.walk(transformed) if isinstance(n, ast3.Assign)]
    assert len(assigns) == 1
    assert isinstance(assigns[0].targets[0], ast3.Name)
    assert assigns[0].targets[0].id == "a"

def test_expression_yield_from_replaced():
    src = """
def g():
    yield from range(5)
"""
    mod = make_module(src)
    transformer = YieldFromTransformer()
    transformed = transformer.visit(mod)
    # No YieldFrom nodes should remain
    for node in ast3.walk(transformed):
        assert not isinstance(node, ast3.YieldFrom)
    # The function body should contain a statement that yields values
    # We check that the body has at least one statement that is not Expr
    body_stmts = transformed.body[0].body
    assert any(not isinstance(stmt, ast3.Expr) for stmt in body_stmts)

def test_no_yield_from_unchanged():
    src = """
def h():
    x = 1
    y = x + 2
"""
    mod = make_module(src)
    transformer = YieldFromTransformer()
    transformed = transformer.visit(mod)
    # The transformed AST should be structurally identical to the original
    original_src = ast_to_source(mod)
    transformed_src = ast_to_source(transformed)
    assert original_src == transformed_src
