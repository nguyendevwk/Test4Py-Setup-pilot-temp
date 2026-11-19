import ast
import typed_ast.ast3 as ast3
import pytest
from py_backwards.transformers.return_from_generator import ReturnFromGeneratorTransformer
from py_backwards.utils.snippet import snippet

def parse_and_transform(code: str) -> ast3.Module:
    """Parse source code to an AST3 module and apply the transformer."""
    tree = ast3.parse(code)
    transformer = ReturnFromGeneratorTransformer()
    transformer.visit(tree)
    return tree

def test_return_replaced_with_exception():
    code = """
def gen():
    yield 1
    return 5
"""
    tree = parse_and_transform(code)
    # Find the function definition
    func = next(node for node in tree.body if isinstance(node, ast3.FunctionDef))
    # The body should now contain a Yield and an exception raise sequence
    body = func.body
    # The first statement should still be the Yield
    assert isinstance(body[0], ast3.Yield)
    # The next statements should be the exception construction and raise
    # We expect three statements: exc = StopIteration(), exc.value = 5, raise exc
    assert len(body) == 3
    exc_assign, value_assign, raise_stmt = body[1], body[2], body[3] if len(body) > 3 else None
    # Check that the exception is created correctly
    assert isinstance(exc_assign, ast3.Assign)
    assert isinstance(exc_assign.value, ast3.Call)
    assert exc_assign.value.func.id == "StopIteration"
    # Check that the value is assigned
    assert isinstance(value_assign, ast3.Assign)
    assert isinstance(value_assign.value, ast3.Constant)
    assert value_assign.value.value == 5
    # Check that the raise statement raises the exception variable
    assert isinstance(raise_stmt, ast3.Raise)
    assert isinstance(raise_stmt.exc, ast3.Name)
    assert raise_stmt.exc.id == "exc"

def test_no_yield_no_transformation():
    code = """
def normal():
    a = 1
    return 2
"""
    tree = parse_and_transform(code)
    func = next(node for node in tree.body if isinstance(node, ast3.FunctionDef))
    # The body should remain unchanged
    assert len(func.body) == 2
    assert isinstance(func.body[0], ast3.Assign)
    assert isinstance(func.body[1], ast3.Return)
    # Ensure the transformer did not mark tree as changed
    transformer = ReturnFromGeneratorTransformer()
    transformer.visit(tree)
    assert not transformer._tree_changed

def test_multiple_returns_and_yield():
    code = """
def multi():
    yield 1
    if True:
        return 3
    else:
        return 4
"""
    tree = parse_and_transform(code)
    func = next(node for node in tree.body if isinstance(node, ast3.FunctionDef))
    # After transformation, there should be two exception raise sequences
    # The body should start with Yield, then first exception sequence, then second
    assert isinstance(func.body[0], ast3.Yield)
    # Find all Raise statements
    raises = [node for node in func.body if isinstance(node, ast3.Raise)]
    assert len(raises) == 2
    # Each raise should raise 'exc'
    for r in raises:
        assert isinstance(r.exc, ast3.Name)
        assert r.exc.id == "exc"
