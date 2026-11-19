import ast
import typed_ast.ast3 as ast3
import pytest
from py_backwards.transformers.return_from_generator import ReturnFromGeneratorTransformer

def _parse_and_transform(code: str) -> ast3.Module:
    """Parse source code, apply transformer, and return the transformed AST."""
    tree = ast3.parse(code)
    transformer = ReturnFromGeneratorTransformer()
    transformed = transformer.visit(tree)
    ast3.fix_missing_locations(transformed)
    return transformed

def _unparse(tree: ast3.Module) -> str:
    """Unparse an AST back to source code."""
    return ast.unparse(tree)

def test_generator_return_replaced():
    """Return in a generator should be replaced with StopIteration exception."""
    src = """
def gen():
    yield 1
    return 5
"""
    transformed = _parse_and_transform(src)
    code = _unparse(transformed)
    assert "yield 1" in code
    assert "return 5" not in code
    assert "raise exc" in code
    assert "exc = StopIteration()" in code
    assert "exc.value = 5" in code

def test_non_generator_return_unchanged():
    """Return in a non-generator function should remain unchanged."""
    src = """
def foo():
    return 10
"""
    transformed = _parse_and_transform(src)
    code = _unparse(transformed)
    assert "return 10" in code
    assert "raise exc" not in code

def test_generator_without_return_stays():
    """Generator without a return should stay unchanged."""
    src = """
def gen():
    yield 1
    yield 2
"""
    transformed = _parse_and_transform(src)
    code = _unparse(transformed)
    assert "yield 1" in code
    assert "yield 2" in code
    assert "return" not in code
    assert "raise exc" not in code
