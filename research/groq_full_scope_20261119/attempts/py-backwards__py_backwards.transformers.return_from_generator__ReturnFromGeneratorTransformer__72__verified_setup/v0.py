import ast
import typed_ast.ast3 as typed_ast
import pytest
from py_backwards.transformers.return_from_generator import ReturnFromGeneratorTransformer


def _parse_and_transform(source: str) -> typed_ast.Module:
    """Parse source with typed_ast and apply the transformer."""
    tree = typed_ast.parse(source)
    transformer = ReturnFromGeneratorTransformer()
    transformer.visit(tree)
    return tree


def _find_function_body(tree: typed_ast.Module) -> list:
    """Return the body list of the first FunctionDef in the module."""
    for node in tree.body:
        if isinstance(node, typed_ast.FunctionDef):
            return node.body
    raise AssertionError("No FunctionDef found")


def test_transformer_replaces_return_in_generator():
    source = """
def gen():
    yield 1
    return 5
"""
    tree = _parse_and_transform(source)
    body = _find_function_body(tree)

    # After transformation, the body should contain a Raise node instead of Return
    assert any(isinstance(stmt, typed_ast.Raise) for stmt in body), "Return not replaced by Raise"

    # The Raise node should raise a StopIteration with value 5
    raise_stmt = next(stmt for stmt in body if isinstance(stmt, typed_ast.Raise))
    exc = raise_stmt.exc
    assert isinstance(exc, typed_ast.Call)
    assert isinstance(exc.func, typed_ast.Name)
    assert exc.func.id == "StopIteration"
    # The StopIteration instance should have its value attribute set
    assert any(
        isinstance(attr, typed_ast.Assign) and
        isinstance(attr.targets[0], typed_ast.Attribute) and
        attr.targets[0].attr == "value" and
        isinstance(attr.value, typed_ast.Num) and
        attr.value.n == 5
        for attr in body
    ), "StopIteration value not set correctly"


def test_transformer_ignores_non_generator_returns():
    source = """
def func():
    return 10
"""
    tree = _parse_and_transform(source)
    body = _find_function_body(tree)

    # The body should still contain a Return node unchanged
    assert any(isinstance(stmt, typed_ast.Return) for stmt in body), "Return was incorrectly transformed"
    return_stmt = next(stmt for stmt in body if isinstance(stmt, typed_ast.Return))
    assert return_stmt.value is not None and isinstance(return_stmt.value, typed_ast.Num) and return_stmt.value.n == 10


def test_transformer_skips_return_without_value_in_generator():
    source = """
def gen():
    yield 2
    return
"""
    tree = _parse_and_transform(source)
    body = _find_function_body(tree)

    # The Return node without a value should remain unchanged
    assert any(isinstance(stmt, typed_ast.Return) for stmt in body), "Return without value was incorrectly removed"
    return_stmt = next(stmt for stmt in body if isinstance(stmt, typed_ast.Return))
    assert return_stmt.value is None, "Return value should be None"
