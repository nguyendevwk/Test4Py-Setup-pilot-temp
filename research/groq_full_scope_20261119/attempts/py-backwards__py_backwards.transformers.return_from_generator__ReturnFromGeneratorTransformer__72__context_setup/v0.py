import ast as pyast
import typed_ast.ast3 as ast
import pytest
from py_backwards.transformers.return_from_generator import ReturnFromGeneratorTransformer

def _parse_and_transform(source: str) -> ast.Module:
    """Parse source with typed_ast and apply the transformer."""
    tree = ast.parse(source)
    transformer = ReturnFromGeneratorTransformer()
    transformer.visit(tree)
    return tree

def test_transformer_replaces_return_in_generator():
    source = """
def gen():
    yield 1
    return 5
"""
    tree = _parse_and_transform(source)
    # Find the function definition
    func = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
    # The body should now contain a Raise node instead of Return
    assert any(isinstance(stmt, ast.Raise) for stmt in func.body)
    # Ensure the Raise node raises a StopIteration with value 5
    raise_stmt = next(stmt for stmt in func.body if isinstance(stmt, ast.Raise))
    exc = raise_stmt.exc
    assert isinstance(exc, ast.Call)
    assert isinstance(exc.func, ast.Name)
    assert exc.func.id == "StopIteration"
    # The exception should have an attribute assignment before the raise
    # The assignment is the previous statement in the body
    assign_stmt = func.body[func.body.index(raise_stmt) - 1]
    assert isinstance(assign_stmt, ast.Assign)
    assert isinstance(assign_stmt.targets[0], ast.Attribute)
    assert assign_stmt.targets[0].attr == "value"
    # The value assigned should be the constant 5
    assert isinstance(assign_stmt.value, ast.Num)
    assert assign_stmt.value.n == 5

def test_transformer_ignores_non_generator_functions():
    source = """
def normal():
    x = 1
    return x
"""
    tree = _parse_and_transform(source)
    func = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
    # The body should still contain a Return node
    assert any(isinstance(stmt, ast.Return) for stmt in func.body)
    # No Raise node should be present
    assert not any(isinstance(stmt, ast.Raise) for stmt in func.body)

def test_transformer_skips_return_without_value():
    source = """
def gen_no_value():
    yield 2
    return
"""
    tree = _parse_and_transform(source)
    func = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
    # The return without value should remain unchanged
    assert any(isinstance(stmt, ast.Return) for stmt in func.body)
    # No Raise node should be present
    assert not any(isinstance(stmt, ast.Raise) for stmt in func.body)
