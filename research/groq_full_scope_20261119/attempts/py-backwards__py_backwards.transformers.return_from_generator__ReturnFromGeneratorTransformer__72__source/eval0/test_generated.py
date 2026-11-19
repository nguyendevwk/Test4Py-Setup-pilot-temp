import ast as pyast
import typed_ast.ast3 as ast
import pytest
from py_backwards.transformers.return_from_generator import ReturnFromGeneratorTransformer

def _parse_and_transform(code: str) -> ast.FunctionDef:
    """Parse the code into a FunctionDef node and apply the transformer."""
    module = ast.parse(code)
    # The module body should contain a single FunctionDef
    func = module.body[0]
    transformer = ReturnFromGeneratorTransformer()
    transformer.visit(module)
    return func

def test_generator_return_replaced_with_raise():
    code = """
def gen():
    yield 1
    return 5
"""
    func = _parse_and_transform(code)
    # After transformation, the last statement should be a Raise
    last_stmt = func.body[-1]
    assert isinstance(last_stmt, ast.Raise)
    # The exception should be a Call to StopIteration
    exc = last_stmt.exc
    assert isinstance(exc, ast.Call)
    assert isinstance(exc.func, ast.Name)
    assert exc.func.id == "StopIteration"
    # The exception should have an attribute assignment for value
    # The body should contain an Assign before the Raise
    assign = func.body[-2]
    assert isinstance(assign, ast.Assign)
    assert isinstance(assign.targets[0], ast.Attribute)
    assert assign.targets[0].attr == "value"
    # The assigned value should be the original return value
    assert isinstance(assign.value, ast.Constant)
    assert assign.value.value == 5

def test_non_generator_function_unchanged():
    code = """
def foo():
    x = 1
    return x
"""
    func = _parse_and_transform(code)
    # The function body should remain unchanged
    assert len(func.body) == 2
    assert isinstance(func.body[0], ast.Assign)
    assert isinstance(func.body[1], ast.Return)
    assert func.body[1].value.value == 1

def test_return_without_value_is_ignored():
    code = """
def gen():
    yield 1
    return
"""
    func = _parse_and_transform(code)
    # The return without value should remain unchanged
    assert any(isinstance(stmt, ast.Return) for stmt in func.body)
    # No Raise should be present
    assert not any(isinstance(stmt, ast.Raise) for stmt in func.body)
